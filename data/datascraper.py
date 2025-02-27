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
