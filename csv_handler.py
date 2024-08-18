from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


# Handles the CSV file
class CSV:
    CSVFILE = "sp500_constituents_by_date.csv"
    COLUMNS = ["Date, Company"]  # Company by ticker
    DATEFORMATNODAY = "%Y-%m"
    DATEFORMAT = "%Y-%m-%d"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSVFILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Date, Company"])
            df.to_csv(cls.CSVFILE, index=False)

    # Gets constituents
    @classmethod
    def get_constituent_data(cls, date, helper=False):
        df = pd.read_csv(cls.CSVFILE)
        df["Date"] = pd.to_datetime(df["Date"], format=CSV.DATEFORMATNODAY)

        start_date = datetime.strptime(date, CSV.DATEFORMATNODAY)

        filteredDf = df[df["Date"] == start_date]["Company"]

        if helper == False:
            if filteredDf.empty:
                print("No data found on the given date")
            else:
                print(
                    filteredDf.astype(str)
                    .apply(lambda x: x.ljust(filteredDf.str.len().max()))
                    .to_string(index=False)
                )

        else:
            return filteredDf

    # Checks if any companies left or joined on a given date
    @classmethod
    def check_change(cls, date):
        start_date = datetime.strptime(date, CSV.DATEFORMATNODAY)
        last = start_date - relativedelta(months=1)
        next = start_date + relativedelta(months=1)

        ldf = CSV.get_constituent_data(last.strftime(cls.DATEFORMATNODAY), True)
        cdf = CSV.get_constituent_data(date, True)
        ndf = CSV.get_constituent_data(next.strftime(cls.DATEFORMATNODAY), True)

        joined = cdf[~cdf.isin(ldf)]
        left = cdf[~cdf.isin(ndf)]

        if joined.empty and left.empty:
            print("\nNo companies joined or left the S&P 500 this month.")
        elif left.empty:
            print("\nNo companies left the S&P 500 this month.")
            print("\nThe following companies joined the S&P 500 this month:")
            print(
                joined.astype(str)
                .apply(lambda x: x.ljust(joined.str.len().max()))
                .to_string(index=False)
            )
        elif joined.empty:
            print("\nNo companies joined the S&P 500 this month.")
            print("\nThe following companies left the S&P 500 this month:")
            print(
                left.astype(str)
                .apply(lambda x: x.ljust(left.str.len().max()))
                .to_string(index=False)
            )
        else:
            print("\nThe following companies joined the S&P 500 this month:")
            print(
                joined.astype(str)
                .apply(lambda x: x.ljust(joined.str.len().max()))
                .to_string(index=False)
            )
            print("\nThe following companies left the S&P 500 this month:")
            print(
                left.astype(str)
                .apply(lambda x: x.ljust(left.str.len().max()))
                .to_string(index=False)
            )

    # Gets all data
    @classmethod
    def get_all_data(cls):
        df = pd.read_csv(cls.CSVFILE)
        return df

    # Filters the CSV file into a given date range
    @classmethod
    def filter_date_range(cls, df, start_date, end_date):
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m")
        filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
        return filtered_df
