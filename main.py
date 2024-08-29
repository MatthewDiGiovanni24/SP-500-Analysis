import yfinance as yf
import matplotlib.pyplot as plt
from data_handler import get_date, plot_by_sector, plot_stock
import csv_handler

# Matthew DiGiovanni
# August 2024
# Analyzes CSV file containing S&P 500 constituents and yfinance data
# Additional analysis by sector

# Example of a draw conclusion:
# The sector with the most amount of S&P 500 companies from 2008-01 to 2019-02 was Financial Services
# This was followed by Consumer Cyclical, Industrials, and Technology


def main():
    while True:
        print(
            "\n1. View and plot data from a company in a requested time period with yfinance"
        )
        print("2. Get S&P 500 constituents at a requested date with csv file")
        print("3. Analyze S&P constituents by sector")
        print("4. Exit")
        choice = input("Enter Choice (1-4): ")

        if choice == "1":
            print("Enter time period (YYYY-MM-DD) or press enter for today")
            ticker = input("Enter ticker: ").upper()
            startDate = get_date("Start date: ", True)
            endDate = get_date("End date: ", True)
            data = yf.download(ticker.strip(), start=startDate, end=endDate)
            print(data)

            toPlot = input("Would you like to plot this data? (y/n): ")

            if toPlot == "y":
                plot_stock(data, ticker)

        elif choice == "2":
            date = get_date(
                "Enter date from 2008-01 to 2019-02 (YYYY-MM): ", False, True
            )
            csv_handler.CSV.get_constituent_data(date)

            joinLeave = input(
                f"\nWould you like to see if any companies joined or left on {date}? (y/n): "
            )

            if joinLeave == "y":
                csv_handler.CSV.check_change(date)

        elif choice == "3":
            start_date = get_date(
                "Start date from 2008-01 to 2019-01 (YYYY-MM): ", False, True
            )
            end_date = get_date(
                "End date from 2008-02 to 2019-02 (YYYY-MM): ", False, True
            )
            print("Loading data...")
            plot_by_sector(csv_handler.CSV.get_all_data(), start_date, end_date)

        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice (1-4)")


if __name__ == "__main__":
    main()
