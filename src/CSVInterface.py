import BankInterface
from datetime import datetime, timedelta
import csv

class CSVInterface(object):
    def __init__(self, bankInterface):
        self.bankInterface: BankInterface = bankInterface
        self.todaysDate: datetime = datetime.date(datetime.now())
        self.weeklySpent = None
        self.weeklyEarned = None
        self.monthlySpent = None
        self.monthlyEarned = None
        self.yearlySpent = None
        self.yearlyEarned = None

    def addDailySpent(self):
        csvWrite: csv = open("./src/data.csv", "a", newline="")
        amountSpent: float = self.bankInterface.getDailySpent()
        csvWriter: csv.writer = csv.writer(csvWrite)
        dailyBudget: float = round(self.bankInterface.getLastPaycheck() / 28, 2)
        csvWriter.writerow([str(self.todaysDate), str(amountSpent), dailyBudget])
        csvWrite.close()

    def getWeeklySpent(self) -> float:
        if self.weeklySpent is None:
            SpentEarned: list = self._getExpensesBudget(7)
            self.weeklySpent = SpentEarned[0]
            self.weeklyEarned = SpentEarned[1]
            return self.weeklySpent
        return self.weeklySpent

    def getMonthlySpent(self) -> float:
        if self.monthlySpent is None:
            SpentEarned: list = self._getExpensesBudget(30)
            self.monthlySpent = SpentEarned[0]
            self.monthlyEarned = SpentEarned[1]
            return self.weeklySpent
        return self.monthlySpent

    def getYearlySpent(self) -> float:
        if self.yearlySpent is None:
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

    # budget for the month or year is money earned * projected earnings

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
        csvRead: csv = open("./src/data.csv", "r")
        csvReader: csv.reader = csv.reader(csvRead)
        for row in csvReader:
            if row and row[0] in datesFromTimeframe:
                currSpent += float(row[1])
                budget += float(row[2])
        csvRead.close()

        projectedEarnings = self._getProjectedEarnings(timeframe)
        budget = projectedEarnings + budget
        return [currSpent, budget]

    def _getProjectedEarnings(self, timeline: int) -> float:
        daysLeft: int = 0
        if timeline == 7:
            daysLeft = 7 - int(self.todaysDate.strftime("%w")) - 1
        if timeline == 30:
            daysLeft = 30 - int(self.todaysDate.strftime("%d"))
        if timeline == 365:
            daysLeft = 365 - int(self.todaysDate.strftime("%j"))
        return round(daysLeft * (self.bankInterface.getLastPaycheck() / 28), 2)

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
            timeframeDate = self.todaysDate - timedelta(
                days=int(self.todaysDate.strftime("%w"))
            )
            for i in range(0, int(self.todaysDate.strftime("%w")) + 1):
                datesFromTimeframe.append(str(timeframeDate + timedelta(days=i)))
        if timeframe == 30:
            # gets nearest past first of the month
            timeframeDate = self.todaysDate - timedelta(
                days=int(self.todaysDate.strftime("%d")) - 1
            )
            for i in range(0, int(self.todaysDate.strftime("%d"))):
                datesFromTimeframe.append(str(timeframeDate + timedelta(days=i)))
        if timeframe == 365:
            # gets nearest past first of the year
            timeframeDate = self.todaysDate - timedelta(
                days=int(self.todaysDate.strftime("%j")) - 1
            )
            for i in range(0, int(self.todaysDate.strftime("%j"))):
                datesFromTimeframe.append(str(timeframeDate + timedelta(days=i)))
        return datesFromTimeframe
