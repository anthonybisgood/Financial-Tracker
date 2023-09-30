import BankInterface
from datetime import datetime, timedelta
import calendar
import csv


class CSVInterface(object):
    def __init__(self, bankInterface: BankInterface):
        self.bankInterface: BankInterface = bankInterface
        self.yesterdaysDate: datetime = datetime.date(datetime.now()) - timedelta(
            days=1
        )
        self.weeklySpent = None
        self.weeklyEarned = None
        self.monthlySpent = None
        self.monthlyEarned = None
        self.yearlySpent = None
        self.yearlyEarned = None

    def addDailySpent(self):
        amountSpent: float = self.bankInterface.getDailySpent()
        dailyBudget: float = self.bankInterface.getDailyBudget()
        csvWrite: csv = open("./data/data.csv", "a", newline="")
        csvWriter: csv.writer = csv.writer(csvWrite)
        self._writeToCSV(
            [str(self.yesterdaysDate), str(amountSpent), dailyBudget],
            csvWriter,
            csvWrite,
        )
        csvWrite.close()

    def getWeeklySpent(self) -> float:
        if self.weeklySpent is None or self.weeklyEarned is None:
            SpentEarned: list = self._getExpensesBudget(7)
            self.weeklySpent = SpentEarned[0]
            self.weeklyEarned = SpentEarned[1]
            return self.weeklySpent
        return self.weeklySpent

    def getMonthlySpent(self) -> float:
        if self.monthlySpent is None or self.monthlyEarned is None:
            SpentEarned: list = self._getExpensesBudget(30)
            self.monthlySpent = SpentEarned[0]
            self.monthlyEarned = SpentEarned[1]
            return self.weeklySpent
        return self.monthlySpent

    def getYearlySpent(self) -> float:
        if self.yearlySpent is None or self.yearlyEarned is None:
            SpentEarned: list = self._getExpensesBudget(365)
            self.yearlySpent = SpentEarned[0]
            self.yearlyEarned = SpentEarned[1]
            return self.yearlySpent
        return self.yearlySpent

    def getWeeklyEarned(self) -> float:
        if self.weeklyEarned is None:
            self.getWeeklySpent()
        return self.weeklyEarned

    def getMonthlyEarned(self) -> float:
        if self.monthlyEarned is None:
            self.getMonthlySpent()
        return self.monthlyEarned

    def getYearlyEarned(self) -> float:
        if self.yearlyEarned is None:
            self.getYearlySpent()
        return self.yearlyEarned

    def _populateDB(self):
        """Internal use only, used to populate data.csv with realistic values"""
        dates: list = []
        yesterdays_date = datetime.date(datetime.now() + timedelta(days=-1))
        for i in range(0, 60):
            dates.append(yesterdays_date - timedelta(i))
        dates.sort()
        EARNED = "57.76"
        csvWrite: csv = open("./data/data.csv", "a", newline="")
        csvWriter: csv.writer = csv.writer(csvWrite)
        for date in dates:
            spent = self.bankInterface.getSpentOnDay(date)
            self._writeToCSV([str(date), str(spent), EARNED], csvWriter, csvWrite)
        csvWrite.close()

    def _writeToCSV(self, toWrite: list, csvWriter, csvWrite):
        # csvWrite: csv = open("./data/data.csv", "a", newline="")
        csvWriter: csv.writer = csv.writer(csvWrite)
        csvWriter.writerow(toWrite)
        # csvWrite.close()

    # budget for the month or year is money earned + projected earnings

    def _getExpensesBudget(self, timeframe: int) -> list:
        """Calculates the budget

        Args:
            timeframe (int): timescale for expenses and budget (7,30,365)

        Returns:
            list:   [0] The amount spent from x days ago to today
                    [1] The budget for the timescale
        """
        currSpent: float = 0
        budget: float = 0
        datesFromTimeframe: list = self.getDays(timeframe)
        csvRead: csv = open("./data/data.csv", "r")
        csvReader: csv.reader = csv.reader(csvRead)
        for row in csvReader:
            if row and row[0] in datesFromTimeframe:
                currSpent += float(row[1])
                budget += float(row[2])
        csvRead.close()
        projectedEarnings = self._getProjectedEarnings(timeframe)
        budget = projectedEarnings + budget
        currSpent = round(currSpent, 2)
        budget = round(budget, 2)
        return [currSpent, budget]

    def _getProjectedEarnings(self, timeline: int) -> float:
        """Calculates the projected earnings for the rest of the week, month or year based on <timeline>

        Args:
            timeline (int): 7, 30, or 365 based of the timeline the program wants

        Returns:
            float: how much money im projected to make for the rest of the year
        """
        daysLeft: int = 0
        if timeline == 7:
            daysLeft = 7 - int(self.yesterdaysDate.strftime("%w")) - 1
        if timeline == 30:
            daysInMonth = calendar.monthrange(
                self.yesterdaysDate.year, self.yesterdaysDate.month
            )[1]
            daysLeft = daysInMonth - int(self.yesterdaysDate.strftime("%d"))
        if timeline == 365:
            daysInYear = 365 + calendar.isleap(datetime.now().year)
            daysLeft = daysInYear - int(self.yesterdaysDate.strftime("%j"))
        return round(daysLeft * (self.bankInterface.getDailyBudget()), 2)

    def getDays(self, timeframe: int) -> list:
        """Gets the days spent from x days ago, to today. Starts from
            nearest sunday, first of the month, or first of the year

        Args:
            timeframe (int): The number of days ago to start counting from

        Returns:
            list: The list of dates from x days ago to today
        """
        datesFromTimeframe: list = []
        if timeframe == 7:
            # gets nearest past sunday
            timeframeDate = self.yesterdaysDate - timedelta(
                days=int(self.yesterdaysDate.strftime("%w"))
            )
            for i in range(0, int(self.yesterdaysDate.strftime("%w")) + 1):
                datesFromTimeframe.append(str(timeframeDate + timedelta(days=i)))
        if timeframe == 30:
            # gets nearest past first of the month
            timeframeDate = self.yesterdaysDate - timedelta(
                days=int(self.yesterdaysDate.strftime("%d")) - 1
            )
            for i in range(0, int(self.yesterdaysDate.strftime("%d"))):
                datesFromTimeframe.append(str(timeframeDate + timedelta(days=i)))
        if timeframe == 365:
            # gets nearest past first of the year
            timeframeDate = self.yesterdaysDate - timedelta(
                days=int(self.yesterdaysDate.strftime("%j")) - 1
            )
            for i in range(0, int(self.yesterdaysDate.strftime("%j"))):
                datesFromTimeframe.append(str(timeframeDate + timedelta(days=i)))
        return datesFromTimeframe
