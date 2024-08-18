from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import io
import sys
from matplotlib import pyplot as plt
import yfinance as yf
import csv_handler

DATEFORMAT = "%Y-%m-%d"
DATEFORMATNODAY = "%Y-%m"

# Gets the date in a valid format
def get_date(prompt, allow_default=False, no_day=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(DATEFORMAT)

    if not no_day:
        try:
            valid_date = datetime.strptime(date_str, DATEFORMAT)
            return valid_date.strftime(DATEFORMAT)
        except ValueError:
            print("Invalid Format (yyyy-mm-dd)")
            return get_date(prompt, allow_default, no_day)

    try:
        valid_date = datetime.strptime(date_str, DATEFORMATNODAY)
        return valid_date.strftime(DATEFORMATNODAY)
    except ValueError:
        print("Invalid Format (yyyy-mm)")
        return get_date(prompt, allow_default, no_day)

# Plots a given stock price
def plot_stock(data, ticker):
    data = data.reset_index()
    dates = list(data["Date"])
    close = list(data["Close"])

    plt.plot(dates, close)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"{yf.Ticker(ticker).info["longName"]} Stock Price")
    plt.show()

# Fetches the ticker from a string
def fetch_ticker_info(ticker):
    try:
        ticker_info = yf.Ticker(ticker).info
        return ticker, ticker_info
    except Exception as e:
        return ticker, None

# Plots constituents by sector
def plot_by_sector(df, start_date, end_date):
    df = csv_handler.CSV.filter_date_range(df, start_date, end_date)
    data = dict()
    unknown_tickers = []

    stderr_backup = sys.stderr
    sys.stderr = io.StringIO()

    tickers = df['Company'].unique()

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ticker = {executor.submit(fetch_ticker_info, ticker): ticker for ticker in tickers}
        
        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                ticker, ticker_info = future.result()
                if ticker_info is None:
                    unknown_tickers.append(ticker)
                else:
                    sector = ticker_info.get('sector', 'Unknown')
                    
                    if sector == 'Unknown':
                        unknown_tickers.append(ticker)
                    else:
                        if sector not in data:
                            data[sector] = 1
                        else:
                            data[sector] += 1
            except Exception as e:
                print(f"Error fetching data for ticker {ticker}: {e}", file=sys.stderr)

    sys.stderr = stderr_backup

    print("Tickers without data on Yahoo Finance: ")
    print(unknown_tickers)
    data.pop('Unknown', None)

    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    plt.figure(figsize=(12, 8))
    plt.bar(sorted_data.keys(), sorted_data.values())
    plt.xlabel("Sector")
    plt.ylabel("Companies")
    plt.title("Companies per Sector in S&P 500 in Given Date Range")
    plt.xticks(rotation=90) 
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()
