import pandas as pd
import matplotlib.pyplot as plt

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
    print("added captical gains")
    df = compute_daily_return(df)
    print("added daily returns")
    df = compute_moving_average(df, 7)
    print("added 7 day MA")
    df = compute_moving_average(df, 14)
    print("added 14 day MA")
    df = compute_moving_average(df, 30)
    print("added 30 day MA")


    return df

df = pd.read_csv("scraped_data.csv", header=0)

df = add_all_technical_indicators(df)

# Drops rows that are missing what we decide are key indicators (FOR NOW TO BE CHANGED LATER)
# final_df_clean = final_df.dropna(subset=['GDP', 'DGS10'])
# final_df_clean = final_df.drop_duplicates()

df = df.drop_duplicates()

# Ensure correct data types
df['Date'] = pd.to_datetime(df['Date'])

#List of columns we assume will be numeric
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'GDP', 'DGS10', 'Capital_Gains', 'Return', 'MA7', 'MA14', 'MA30', 'FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7', 'FF8', 'FF9', 'FF10', 'FF11', 'FF12', 'FF13', 'FFavg']
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Sort data by Ticker and Date (FOR NOW TO BE CHANGED LATER)
final_df_clean = df.sort_values(by=['Ticker', 'Date']).reset_index(drop=True)

# Verify the data types
#print(final_df_clean.info())

# Get summary to understand distributions 
#print(final_df.describe())

# See how many missing values exist in each column
#print(final_df.isnull().sum())

final_df_clean.to_csv('cleaned_data.csv', index=False)

#Data Visuzalization
# plt.figure(figsize=(12, 8))
# for ticker in final_df_clean['Ticker'].unique():
#     ticker_data = final_df_clean[final_df_clean['Ticker'] == ticker]
#     plt.plot(ticker_data['Date'], ticker_data['Close'], label=ticker)

# plt.xlabel("Date")
# plt.ylabel("Close Price")
# plt.title("Close Price Over Time for All Tickers")
# plt.xticks(rotation=45)
# plt.legend(loc='upper left', bbox_to_anchor=(1, 1)) 
# plt.tight_layout()
# plt.show()


# HERE - Do Correlation Analysis

# HERE - Feature Selection