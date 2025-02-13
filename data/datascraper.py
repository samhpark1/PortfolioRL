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

# Drops rows that are missing what we decide are key indicators (FOR NOW TO BE CHANGED LATER)
final_df_clean = final_df.dropna(subset=['GDP', 'DGS10', 'FEDFUNDS', 'Capital Gains'])
final_df_clean = final_df.drop_duplicates()

# Ensure correct data types
final_df_clean['Date'] = pd.to_datetime(final_df_clean['Date'])

#List of columns we assume will be numeric
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'GDP', 'DGS10', 'FEDFUNDS']

for col in numeric_columns:
    if col in final_df_clean.columns:
        final_df_clean[col] = pd.to_numeric(final_df_clean[col], errors='coerce')
        
# Sort data by Ticker and Date (FOR NOW TO BE CHANGED LATER)
final_df_clean = final_df_clean.sort_values(by=['Ticker', 'Date']).reset_index(drop=True)

# Verify the data types
print(final_df_clean.info())

# Get summary statistics to understand distributions and outliers
#print(final_df.describe())

# See how many missing values exist in each column
#print(final_df.isnull().sum())
