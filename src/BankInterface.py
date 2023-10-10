from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
import MintConnection

PAYCHECK_ALLOCATED_TO_EXPENSES = 2 / 3
TIME_BETWEEN_PAYCHECKS = 14


class BankInterface(object):
    def __init__(self, mint: MintConnection):
        # create link to bank account and login, get account info
        self.dailySpent = None
        self.lastPaycheck = None
        self.mint = mint
        self.mintConn = self.mint.getMintConn()
        self.accounts = self._getAccountData()
        self.tr_df = None
        self.getLastPaycheck()
        self.getDailySpent()

    def getDailySpent(self) -> float:
        """returns the amount spent yesterday

        Returns:
            float: amount spent yesterday
        """
        if self.dailySpent is None:
            yesterday = datetime.date(datetime.now()) - timedelta(days=1)
            self.dailySpent = self.getSpentOnDay(yesterday)
        return self.dailySpent

    def getLastPaycheck(self) -> float:
        """Get the last paycheck amount

        Returns:
            float: last paycheck amount
        """
        if self.lastPaycheck is None:
            self.lastPaycheck = self._get_last_paycheck()
        return self.lastPaycheck

    def getDailyBudget(self) -> float:
        allocatedExpenses = round(
            self.lastPaycheck * (PAYCHECK_ALLOCATED_TO_EXPENSES), 2
        )
        dailyBudget = round(allocatedExpenses / TIME_BETWEEN_PAYCHECKS, 2)
        return dailyBudget

    def getSpentOnDay(self, date: datetime):
        credit_account_ids = self._getCreditAccounts()
        totalSpent: float = 0
        for account_id in credit_account_ids:
            transactions = self._get_account_transactions(account_id)
            transactions = transactions.loc[
                transactions["date"] == (date).strftime("%Y-%m-%d")
            ]
            if "description" in transactions.columns:
                transactions = transactions[
                    transactions["description"].apply(
                        lambda x: isinstance(x, str) and "Payment" not in x
                    )
                ]
                if not transactions.empty:
                    totalSpent += transactions.get("amount").sum()
        totalSpent = round(totalSpent, 2) * -1
        if totalSpent == 0:
            totalSpent = 0.00
        return totalSpent

    def _get_last_paycheck(self) -> float:
        checkings_account_ids = self._getDebitAccounts()
        last_paycheck = -1
        for account_id in checkings_account_ids:
            account_transactions: pd.DataFrame = self._get_account_transactions(
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
        accounts = self.accounts
        checking_account_ids = accounts.loc[
            accounts["bankAccountType"] == "CHECKING", "id"
        ].tolist()

        return checking_account_ids

    def _getCreditAccounts(self) -> list[str]:
        accounts = self.accounts
        credit_account_ids = accounts.loc[
            accounts["name"] == "CREDIT CARD", "id"
        ].tolist()
        return credit_account_ids

    def _getAccountData(self) -> pd.DataFrame:
        """Returns a dataframe of the accounts data

        Returns:
            pd.DataFrame: dataframe of the accounts data
        """
        account_data = self.mintConn.get_account_data()
        ad_df = pd.DataFrame(account_data)
        return ad_df

    def _get_account_transactions(self, account_id) -> pd.DataFrame:
        if self.tr_df is None:
            self.tr_df = pd.DataFrame(
                self.mintConn.get_transaction_data(remove_pending=False)
            )
        account_transactions: pd.DataFrame = self.tr_df.loc[
            self.tr_df["accountId"] == account_id
        ]
        return account_transactions
