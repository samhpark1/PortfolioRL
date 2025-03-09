import yfinance as yf
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os
from collections import OrderedDict



def getTickerInfo(df):
    for tick in tickers:
        if all_data_exists and ((df['Ticker'] == tick) & (df['Date'] == start_date) & (df['Date'] == end_date)).any():
            continue
        else:
            try:
                ticker = yf.Ticker(tick)
                data = ticker.history(start=start_date, end=end_date, interval=time_interval)
                 # Reset index to store the date as a column
                data.reset_index(inplace=True)

                data['Ticker'] = tick
                df = pd.concat([df, data])
                data['Ticker'] = tick
                df = pd.concat([df, data])
                print(f'Finished retreiving {tick} data')
            except Exception as e:
                final_df.to_csv('interim.csv', index=False)
                print(str(e))

#load FRED api key
load_dotenv()

## Ticker data (company specific)

# load csv of tickers
ticker_df = pd.read_csv("tickers.csv", header=0)
tickers = ticker_df['Ticker'].to_list()

#get data from list of tickers
df = pd.DataFrame()

time_period = '1y'
time_interval = '1d'
start_year = 2018
end_year = 2024

start_date = f"{start_year}-01-01"
end_date = f"{end_year}-12-31"

all_data_exists = os.path.exists("all_data.csv")
if all_data_exists:
    df = pd.read_csv("all_data.csv")
start_year = 2018
end_year = 2024

start_date = f"{start_year}-01-01"
end_date = f"{end_year}-12-31"

all_data_exists = os.path.exists("all_data.csv")
if all_data_exists:
    df = pd.read_csv("all_data.csv")

for tick in tickers:
    if all_data_exists and ((df['Ticker'] == tick) & (df['Date'] == start_date) & (df['Date'] == end_date)).any():
        continue
    else:
        ticker = yf.Ticker(tick)
        data = ticker.history(start=start_date, end=end_date, interval=time_interval)


    # Reset index to store the date as a column
        data.reset_index(inplace=True)

        data['Ticker'] = tick
        df = pd.concat([df, data])
        data['Ticker'] = tick
        df = pd.concat([df, data])


    
    return df

def getFedFundsData():
    try:
        fedFundsSeries = fred.get_series("FEDFUNDS", observation_start=f"{start_year-1}-01-01", observation_end=f"{end_year}-12-31")
        for i, v in fedFundsSeries.items():
            FedFundLoc[str(i)[:7]] = len(FedFundOrder)
            FedFundOrder.append(v)
    except Exception as e:
        print(str(e))


def addPrevYearFF(row):
    loc = FedFundLoc[row['Date'][:7]]
    hist = FedFundOrder[loc - 12: loc+1]
    for i in range(len(hist)):
        row[f'FF{i+1}'] = hist[i]
    
    row['FFavg'] = sum(hist)/len(hist)

    return row

def addMacroData(row):
    year = row['Date'][0:4]
    
    if year not in FRED_by_year.keys():
        FRED_by_year[year] = {}
        for indicator in macro_indicators:
            try:
                series_data = fred.get_series(indicator, observation_start=f"{year}-01-01", observation_end=f"{year}-12-31")
                FRED_by_year[year][indicator] = series_data.mean() if not series_data.empty else None
            except Exception as e:
                FRED_by_year[year][indicator] = None  # Handle missing data
    
    for indicator in macro_indicators:
        row[indicator] = FRED_by_year[year].get(indicator, None)
        
    
    
    return row


#load FRED api key
load_dotenv()

#Add macroeconomic indicators to df with company info
final_df = df.apply(addMacroData, axis=1)


def add_capital_gains(df):
    #Calculated as the percentage change from the Open to Close price
    df['Capital_Gains'] = (df['Close'] - df['Open']) / df['Open']
    return df

def compute_daily_return(df):
    #Calculated as the percentage change in Close price for each ticker
    df = df.sort_values(by=['Ticker', 'Date'])
    df['Return'] = df.groupby('Ticker')['Close'].pct_change()
    return df

def compute_moving_average(df, window, column='Close'):
    #Computes a moving average for a given window over the specified column
    #The result is stored in a new column  (MA{window})
    ma_column = f"MA{window}"
    df[ma_column] = df.groupby('Ticker')[column].transform(lambda x: x.rolling(window=window).mean())
    return df


def add_all_technical_indicators(df):
  
    df = add_capital_gains(df)
    df = compute_daily_return(df)
    df = compute_moving_average(df, 7)
    df = compute_moving_average(df, 14)
    df = compute_moving_average(df, 30)
  
    return df

final_df = add_all_technical_indicators(final_df)
final_df.to_csv('all_data.csv', index=False)

# Drops rows that are missing what we decide are key indicators (FOR NOW TO BE CHANGED LATER)
final_df_clean = final_df.dropna(subset=['GDP', 'DGS10', 'FEDFUNDS'])
final_df_clean = final_df.drop_duplicates()

# Ensure correct data types
final_df_clean['Date'] = pd.to_datetime(final_df_clean['Date'])

#List of columns we assume will be numeric
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'GDP', 'DGS10', 'FEDFUNDS', 'Capital_Gains', 'Return', 'MA7', 'MA14', 'MA30']
for col in numeric_columns:
    if col in final_df_clean.columns:
        final_df_clean[col] = pd.to_numeric(final_df_clean[col], errors='coerce')
        
# Sort data by Ticker and Date (FOR NOW TO BE CHANGED LATER)
final_df_clean = final_df_clean.sort_values(by=['Ticker', 'Date']).reset_index(drop=True)

# Verify the data types
#print(final_df_clean.info())


## Ticker data (company specific)

# load csv of tickers
ticker_df = pd.read_csv("tickers.csv", header=0)
tickers = ticker_df['Ticker'].to_list()

#get data from list of tickers
df = pd.DataFrame()

time_interval = '1d'
start_year = 2022
end_year = 2024

start_date = f"{start_year}-01-01"
end_date = f"{end_year}-12-31"

all_data_exists = os.path.exists("all_data.csv")
if all_data_exists:
    df = pd.read_csv("all_data.csv")


## Macroeconomic data (GDP, interest, etc)
fred = Fred(api_key=os.getenv("FRED_API_KEY")) #API key from https://fred.stlouisfed.org/docs/api/api_key.html
macro_indicators = ['GDP', 'DGS10']
FRED_by_year = {}
FedFundLoc = OrderedDict()
FedFundOrder = []

ticker_df = getTickerInfo(df)
getFedFundsData()


ticker_df['Date'] = ticker_df['Date'].astype(str)

#Add macroeconomic indicators to df with company info
final_df = ticker_df.apply(addMacroData, axis=1)
final_df = ticker_df.apply(addPrevYearFF, axis=1)

final_df.to_csv('scraped_data.csv', index=False)
#HERE - Feature Selection

