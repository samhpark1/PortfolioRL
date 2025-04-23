from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd



load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_total_close_prices(tickers: list[str]):
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=30)

    # Fetch data
    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        interval="1d",
        group_by='ticker',
        auto_adjust=True,
        progress=False
    )

    print(data)


    if len(tickers) == 1:
        close_df = data[['Close']].rename(columns={'Close': tickers[0]})
    else:
        close_df = pd.concat([data[ticker]['Close'].rename(ticker) for ticker in tickers], axis=1)

    close_df.dropna(how='all', inplace=True)

    summed = close_df.sum(axis=1)

    print(close_df)
    print(summed)

    result = [
        {"time": idx.strftime("%Y-%m-%d"), "value": round(val, 2)}
        for idx, val in summed.items()
    ]

    return result

@app.route("/api/hist", methods=["POST"])
def get_portfolio_hist():
    data = request.get_json()

    tickers = [stock[0] for stock in data]

    return get_total_close_prices(tickers)

    

if __name__ == "__main__":
    app.run(debug=True)