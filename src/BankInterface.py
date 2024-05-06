from datetime import datetime, timedelta
import sqlite3
import pandas as pd
from dotenv import load_dotenv


PAYCHECK_ALLOCATED_TO_EXPENSES = 2 / 3
TIME_BETWEEN_PAYCHECKS = 14


class BankInterface(object):
    def __init__(self, cursor: sqlite3.Cursor):
        # create link to bank account and login, get account info
        self.cursor = cursor

    def getSpentYesterday(self) -> float:
        """returns the amount spent yesterday

        Returns:
            float: amount spent yesterday
        """
        return self.getSpentOnDay(datetime.date(datetime.now()) - timedelta(days=1))
        
    def getLastPaycheck(self) -> float:
        """Get the last paycheck amount

        Returns:
            float: last paycheck amount
        """
        last_paycheck = self.cursor.execute(
            "SELECT MAX(date) FROM TRANSACTIONS WHERE payee like '%Payment Thank You-Mobile%'"
        )
        
        return last_paycheck

    def getDailyBudget(self) -> float:
        allocatedExpenses = round(
            (self.lastPaycheck * (PAYCHECK_ALLOCATED_TO_EXPENSES)) - 100, 2
        )
        dailyBudget = round(allocatedExpenses / TIME_BETWEEN_PAYCHECKS, 2)
        return dailyBudget

    def getSpentOnDay(self, date: datetime, accounts: list[str]) -> float:
        """returns the amount spent on a given day

        Args:
            date (datetime): date to get amount spent on

        Returns:
            float: amount spent on the given day
            
        """
        total = 0
        for account in accounts:
            self.cursor.execute(
                "SELECT SUM(amount) FROM TRANSACTIONS WHERE date = ? and accountID = ? and payee not like '%Payment Thank You-Mobile%'",
                (
                    date,
                    account,
                ),
            )
            spent = self.cursor.fetchone()[0]
            if spent is not None:
                total += spent
        if total is None:
            return 0
        return total

    def _get_last_paycheck(self) -> float:
        checkings_account_ids = self._getAccountIDs("checking")
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

    def _getAccountIDs(self, accountType: str) -> list[str]:
        """gets account IDs of a given type

        Args:
            accountType (str): type of account "checking", "creditCard", "savings"

        Returns:
            list[str]: returns a list of account IDs of the given type
        """
        self.cursor.execute(
            "SELECT accountID FROM ACCOUNTS WHERE accountType = ?", (accountType,)
        )
        return [account[0] for account in self.cursor.fetchall()]

    def _get_account_transactions(self, account_id) -> pd.DataFrame:
        """Returns a dataframe of the transactions for a given account"""
        pass
    
    def getEarnedBetween(startDate: datetime, endDate: datetime) -> float:
        
        pass
        

