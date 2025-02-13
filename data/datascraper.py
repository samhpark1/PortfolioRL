import yfinance as yf
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv
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

for tick in tickers:
    ticker = yf.Ticker(tick)
    data = ticker.history(period=time_period, interval=time_interval)

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
final_df.to_csv('all_data.csv', index=False)




    