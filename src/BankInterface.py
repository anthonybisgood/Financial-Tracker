import os

import datetime as dt
from dotenv import load_dotenv
import mintapi
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# Replace 'path_to_chromedriver' with the actual path to your ChromeDriver executable


class MintConnection(object):
    def __init__(self):
        load_dotenv()

    def getMintConn(self) -> mintapi.Mint:
        password = os.getenv("MINT_PASS")
        mint = mintapi.Mint(
            "abisgood10@gmail.com",
            password,
            wait_for_sync=False,
            wait_for_sync_timeout=500,
            mfa_method="sms",
        )
        return mint

    def closeMintConn(self, mint: mintapi.Mint):
        mint.close()


class BankInterface(object):
    def __init__(self, mintConn: mintapi.Mint):
        # create link to bank account and login, get account info
        self.dailySpent = None
        self.lastPaycheck = None
        self.mintConn = mintConn
        self.accounts = self.getAccountData()
        self.tr_df = None
        pass

    def getDailySpent(self) -> float:
        """returns the amount spent yesterday

        Returns:
            float: amount spent yesterday
        """
        if self.dailySpent is None:
            self.dailySpent = self._get_yesterdays_spent()
        return self.dailySpent

    def getLastPaycheck(self) -> float:
        """Get the last paycheck amount

        Returns:
            float: last paycheck amount
        """
        if self.lastPaycheck is None:
            self.lastPaycheck = self._get_last_paycheck()
        return self.lastPaycheck

    def _get_yesterdays_spent(self) -> float:
        """Uses mint api to get yesterdays transactions and calculates total spent

        Returns:
            _type_: _description_
        """
        credit_account_ids = self._getCreditAccounts()
        totalSpent: float = 0
        for account_id in credit_account_ids:
            transactions = self.get_account_transactions(account_id)
            transactions = transactions.loc[
                transactions["date"]
                == (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            ]
            totalSpent = transactions["amount"].sum()
        return totalSpent

    def _get_last_paycheck(self) -> float:
        checkings_account_ids = self._getDebitAccounts()
        last_paycheck = -1
        for account_id in checkings_account_ids:
            account_transactions: pd.DataFrame = self.get_account_transactions(
                account_id
            )
            if "category" in account_transactions.columns:
                paycheck_df = account_transactions[
                    account_transactions["category"].apply(
                        lambda x: isinstance(x, dict) and x.get("name") == "Paycheck"
                    )
                ]
                last_paycheck = paycheck_df.iloc[0]["amount"]
        return last_paycheck

    def _getDebitAccounts(self) -> list[str]:
        accounts = self.mintConn.get_account_data()
        accountIDs = []
        for account in accounts:
            if account["name"] == "CHASE SAVINGS":
                accountIDs.append(account["id"])
        return accountIDs

    def _getCreditAccounts(self) -> list[str]:
        accounts = self.mintConn.get_account_data()
        accountIDs = []
        for account in accounts:
            if account["name"] == "CREDIT CARD":
                accountIDs.append(account["id"])
        return accountIDs

    def getAccountData(self) -> pd.DataFrame:
        account_data = self.mintConn.get_account_data()
        ad_df = pd.DataFrame(account_data)
        return ad_df

    def get_account_transactions(self, account_id):
        tr_df = pd.DataFrame(self.mintConn.get_transaction_data(remove_pending=False))
        self.tr_df = tr_df
        account_transactions = tr_df.loc[tr_df["accountId"] == account_id]
        return account_transactions


def main():
    mintConn = MintConnection()
    mint = mintConn.getMintConn()
    bi = BankInterface(mint)
    yesterday_spent = bi.getDailySpent()
    print("Yesterday spent: {}".format(yesterday_spent))
    last_paycheck = bi.getLastPaycheck()
    print("Last paycheck: {}".format(last_paycheck))
    mintConn.closeMintConn(mint)


main()
