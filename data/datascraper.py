import yfinance as yf
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os


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


## Macroeconomic data (GDP, interest, etc)
fred = Fred(api_key=os.getenv("FRED_API_KEY")) #API key from https://fred.stlouisfed.org/docs/api/api_key.html
macro_indicators = ['GDP', 'DGS10', 'FEDFUNDS']
FRED_by_year = {}

def addMacroData(row):
    year = row['Date'].year
    
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

# Get summary to understand distributions 
#print(final_df.describe())

# See how many missing values exist in each column
#print(final_df.isnull().sum())

#Data Visuzalization
plt.figure(figsize=(12, 8))
for ticker in final_df_clean['Ticker'].unique():
    ticker_data = final_df_clean[final_df_clean['Ticker'] == ticker]
    plt.plot(ticker_data['Date'], ticker_data['Close'], label=ticker)

plt.xlabel("Date")
plt.ylabel("Close Price")
plt.title("Close Price Over Time for All Tickers")
plt.xticks(rotation=45)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1)) 
plt.tight_layout()
plt.show()


#HERE - Do Correlation Analysis

#HERE - Feature Selection