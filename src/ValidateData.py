import pandas as pd
from datetime import datetime, timedelta
from CSVInterface import CSVInterface
# if date not there, if date changed

TEMP_DATA = pd.read_csv("./data/transactions.csv")


class ValidateData(object):
    def __init__(self, bankInterface, csvInterface: CSVInterface):
        self.bankInterface = bankInterface
        self.csvInterface = csvInterface

    def fillInMissingDates(self):
        with open("./data/data.csv", "r") as csv:
            data = csv.readlines()
            lastRow = data[-1]
            csv.close()
        date = lastRow.split(",")[0]
        start_date = datetime.strptime(date, "%Y-%m-%d").date() + timedelta(days=1)
        end_date = datetime.date(datetime.now()) - timedelta(days=1)
        date_list = []
        current_date = start_date
        while current_date < end_date:
            date_list.append(current_date)
            current_date += timedelta(days=1)
        for date in date_list:
            self.csvInterface.addDailySpent(date)

    # def validate(self):
    #     # check if data is there
    #     # check if data is correct
    #     # transactions = self.getTransactions()
    #     transactions = TEMP_DATA
    #     dates = self.datesToValidate()
    #     with open("./data/data.csv", "r") as csv:
    #         data = csv.readlines()
    #         rows = data[-8:]
    #         for row in rows:
        
    
    def getTransactions(self) -> pd.DataFrame:
        accounts = self.bankInterface._getCreditAccounts()
        transactions = pd.DataFrame()
        for account in accounts:
            transaction = self.bankInterface._get_account_transactions(account)
            transactions = pd.concat([transactions, transaction]).sort_values(by="date")
        transactions.to_csv("./data/transactions.csv")
        return transactions

    def checkIfDatesThere(self):
        csvRead = open("./data/data.csv", "r")

    def datesToValidate(self):
        dates = []
        for i in range(2, 10):
            dates.append(datetime.date(datetime.now() - timedelta(days=i)))
        return dates
