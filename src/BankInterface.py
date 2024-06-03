from datetime import datetime, timedelta
import sqlite3

TIME_BETWEEN_PAYCHECKS = 14


class BankInterface(object):
    def __init__(self, cursor: sqlite3.Cursor):
        # create link to bank account and login, get account info
        self.cursor = cursor

    def getSpentYesterday(self) -> float:
        """returns the amount spent yesterday on credit and checking accounts

        Returns:
            float: amount spent yesterday
        """
        accounts: list[str] = self._getAccountIDs("checking")
        accounts.extend(self._getAccountIDs("creditCard"))
        return self.getSpentOnDay(
            datetime.date(datetime.now()) - timedelta(days=1), accounts
        )

    def getLastPaycheck(self) -> float:
        """Get the last paycheck amount including if I get a bonus on that day, does not include money taken out for robinhood

        Returns:
            float: last paycheck amount
        """
        last_paycheck_date = self.getLastPaycheckDate()
        last_paycheck = self.cursor.execute(
            "SELECT SUM(amount) from TRANSACTIONS WHERE Date = ? and payee like '%PAYROLL%'",
            (last_paycheck_date,),
        )
        amount = last_paycheck.fetchone()[0]
        if amount is None:
            return 0
        return amount

    def getLastPaycheckDate(self) -> str:
        last_date = self.cursor.execute(
            "SELECT max(date) FROM transactions WHERE payee like '%PAYROLL%'"
        )
        last_date = last_date.fetchone()[0]
        return last_date

    def getFirstPaycheckDateAfter(self, start) -> datetime:
        first_date = self.cursor.execute(
            "SELECT min(date) FROM transactions WHERE payee like '%PAYROLL%' and date >= ?",
            (start,),
        )
        first_date = first_date.fetchone()[0]
        # i.e if its the 3rd, no paycheck the first and second, so return the last paycheck
        if first_date is None:
            return None
        first_date = datetime.strptime(first_date, "%Y-%m-%d").date()
        return first_date

    def getFirstPaycheckDateBefore(self, date: datetime) -> datetime:
        first_date = self.cursor.execute(
            "SELECT max(date) FROM transactions WHERE payee like '%PAYROLL%' and date <= ?",
            (date,),
        )
        first_date = first_date.fetchone()[0]
        if first_date is None:
            return None
        first_date = datetime.strptime(first_date, "%Y-%m-%d").date()
        return first_date

    def getDailyBudget(self, end: datetime) -> float:
        start = self.getLastPaycheckDate()
        utils = -self.getSpentBetween(self._getAccountIDs("checking"), start, end)
        earned = self.getEarnedBetween(self._getAccountIDs("checking"), start, end)
        dailyBudget = (earned - utils) / TIME_BETWEEN_PAYCHECKS
        return dailyBudget

    def getSpentOnDay(self, date: datetime, accounts: list[str]) -> float:
        """returns the amount spent on a given day by credit accounts

        Args:
            date (datetime): date to get amount spent on

        Returns:
            float: amount spent on the given day

        """
        total = 0
        for account in accounts:
            self.cursor.execute(
                "SELECT SUM(amount) FROM TRANSACTIONS WHERE date = ? and accountID = ? and payee not in ('%Payment Thank You-Mobile%', '%Robinhood%', '%Zelle payment to Dad%')",
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

    def getEarnedOn(self, date: datetime) -> float:
        """returns the amount earned on a given day after utils

        Args:
            date (datetime): date to get amount earned on

        Returns:
            float: amount earned on the given day
        """
        accounts = self._getAccountIDs("checking")
        utils = -self.getSpentBetween(accounts, date, date)
        earned = self.getEarnedBetween(accounts, date, date)
        return earned - utils

    def getEarnedBetween(
        self, accounts: list[str], startDate: datetime, endDate: datetime
    ) -> float:
        """get gets the amount earned between two dates inclusive, exclusive

        Args:
            accounts (list[str]): accounts to get amount earned from
            startDate (datetime): start date inclusive
            endDate (datetime): end date exclusive

        Returns:
            float: amount earned between the two dates
        """
        normalized_accounts = tuple(accounts)
        placeholders = ", ".join(["?"] * len(normalized_accounts))
        query = f"select sum(amount) from transactions where accountID IN ({placeholders}) and date between ? and ? and amount > 0"
        self.cursor.execute(query, normalized_accounts + (startDate, endDate))
        amount = self.cursor.fetchone()[0]
        return amount if amount is not None else 0

    def getSpentBetween(
        self, accounts: list[str], startDate: datetime, endDate: datetime
    ) -> float:
        """get gets the amount spent between two dates inclusive, exclusive

        Args:
            accounts (list[str]): accounts to get amount spent from
            startDate (datetime): start date inclusive
            endDate (datetime): end date exclusive

        Returns:
            float: amount spent between the two dates
        """
        normalized_accounts = tuple(accounts)
        placeholders = ", ".join(["?"] * len(normalized_accounts))
        query = f"select sum(amount) from transactions where accountID IN ({placeholders}) and date between ? and ? and amount < 0 and payee not like '%Payment to Chase card%'"
        self.cursor.execute(
            query,
            normalized_accounts
            + (
                startDate,
                endDate,
            ),
        )
        amount = self.cursor.fetchone()[0]
        return amount if amount is not None else 0

    def getProjectedBudget(self, startDate, endDate) -> float:
        money_before = self._getMoneyBefore(startDate)
        paychecks = self.getPaychecksBetween(startDate, endDate)
        predicted = self._predictPaychecks(endDate)
        total = money_before + paychecks + predicted
        print("money before", money_before, "paychecks", paychecks, "predicted", predicted)
        return round(total, 2)

    def _getMoneyBefore(self, start) -> float:
        first_paycheck_date = self.getFirstPaycheckDateAfter(start)
        # if theres no paychecks within the range, it'll return 0
        if first_paycheck_date is None:
            return 0
        first_paycheck_before = self.getFirstPaycheckDateBefore(start)
        first_paycheck_amount = self.getEarnedOn(first_paycheck_before)
        time_between = abs((start - first_paycheck_date).days)
        dailyBudget = (first_paycheck_amount) / TIME_BETWEEN_PAYCHECKS
        unallocated_budget = dailyBudget * time_between
        return round(unallocated_budget, 2)

    def _predictPaychecks(self, endDate) -> float:
        last_paycheck_date = self.getFirstPaycheckDateBefore(endDate)
        difference_inclusive = abs((endDate - last_paycheck_date).days + 1)
        amount = self.getEarnedOn(last_paycheck_date)
        predicted = ((amount) / TIME_BETWEEN_PAYCHECKS) * difference_inclusive
        return round(predicted, 2)

    def getPaychecksBetween(self, startDate, endDate) -> float:
        """Get the sum of all paychecks between two dates, if there's only 1, return 0
        Args:
            startDate (_type_): _description_
            endDate (_type_): _description_

        Returns:
            float: _description_
        """
        count = self._exectuteQuery(
            "SELECT COUNT(*) from TRANSACTIONS WHERE Date between ? and ? and payee like '%PAYROLL%'",
            (startDate, endDate),
        )[0]
        if count <= 1:
            return 0
        amount = self._exectuteQuery(
            "SELECT SUM(amount) from TRANSACTIONS WHERE Date between ? and ? and payee like '%PAYROLL%'",
            (startDate, endDate),
        )[0]
        last_paycheck_date = self._exectuteQuery(
            "SELECT max(date) FROM transactions WHERE payee like '%PAYROLL%' and date < ?",
            (endDate,),
        )[0]
        last_paycheck_amount = self.getEarnedOn(last_paycheck_date)
        amount -= last_paycheck_amount
        return amount if amount else 0

    def _getMoneyBeforeFirstPaycheck(
        self, startDate: datetime, first_paycheck_date: datetime
    ) -> float:
        """Gets the money earned from the start date to the first paycheck date
        END DATE MUST BE AFTER STARTDATE, END DATE MUST BE BEFORE OR EQUAL TO A PAYCHECK DATE

        Args:
            startDate (datetime): date
            first_paycheck_date (datetime): paycheck date

        Returns:
            float: _description_
        """
        if startDate == first_paycheck_date:
            return 0.00
        last_paycheck_date = self.getFirstPaycheckDateBefore(startDate)
        last_paycheck_amount = self.getEarnedOn(last_paycheck_date)
        time_between = abs((startDate - first_paycheck_date).days - 1)
        dailyBudget = (last_paycheck_amount) / TIME_BETWEEN_PAYCHECKS
        unallocated_budget = dailyBudget * time_between
        return unallocated_budget

    def _exectuteQuery(self, query: str, args: tuple) -> any:
        self.cursor.execute(query, args)
        result = self.cursor.fetchone()
        return result
