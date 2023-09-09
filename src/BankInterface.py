import os
from datetime import datetime, timedelta
import mintapi
from pathlib import Path
import pandas as pd


class BankInterface(object):
    def __init__(self):
        # create link to bank account and login, get account info
        self.dailySpent = None
        self.lastPaycheck = None
        self.mintConn = MintConnection()
        pass

    def getDailySpent(self) -> float:
        # So we only fetch once
        if not self.dailySpent:
            self.dailySpent = self.mintConn.get_yesterdays_transations
        return self.dailySpent

    def getLastPaycheck(self) -> float:
        if not self.lastPaycheck:
            self.lastPaycheck = self.mintConn.get_last_paycheck
        # Do This later, This would be the biweekly paycheck amount
        return self.lastPaycheck


class MintConnection(object):
    def __init__(self):
        password = "get from env"
        self.mint = mintapi.Mint(
            "abisgood30@gmail.com",
            password,
        )

    def get_yesterdays_spent(self):
        transactions: pd.DataFrame = self._get_yesterdays_transations()
        totalSpent: float = None
        # TODO calc total spent from dataframe
        return totalSpent

    def _get_yesterdays_transations(self):
        yesterday = datetime.date(datetime.now() - timedelta(days=1))
        transactionData: pd.DataFrame = self.mint.get_transaction_data(yesterday, yesterday)
        return transactionData

    def get_last_paycheck(self):
        # TODO use mint api logic last paycheck to chase savings account
        return 1643


def main():
    x = MintConnection()


main()
