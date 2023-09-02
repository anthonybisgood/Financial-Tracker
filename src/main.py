import csv
from datetime import datetime, timedelta
import calendar

PERCENT_SAVINGS = 0.5


class BankInterface(object):
    def __init__(self):
        # create link to bank account and login, get account info
        self.dailySpent = None
        self.lastPaycheck = None
        pass

    def getDailySpent(self) -> float:
        # So we only fetch once
        if not self.dailySpent:
            self.dailySpent = self.fetchDailySpent()
            return self.dailySpent
        return self.dailySpent

    def fetchDailySpent(self):
        # Get daily spent from bank account
        return 50.0

    def getLastPaycheck(self) -> float:
        if not self.lastPaycheck:
            self.lastPaycheck = self.fetchLastPaycheck()
            return self.lastPaycheck
        # Do This later, This would be the biweekly paycheck amount
        return self.lastPaycheck

    def fetchLastPaycheck(self):
        # Get last paycheck from bank account
        return 1648.55


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
        if not self.weeklySpent:
            SpentEarned: list = self.getExpenses_Budget(7)
            self.weeklySpent = SpentEarned[0]
            self.weeklyEarned = SpentEarned[1]
            return self.weeklySpent
        return self.weeklySpent

    def getMonthlySpent(self) -> float:
        if not self.monthlySpent:
            SpentEarned: list = self.getExpenses_Budget(30)
            self.monthlySpent = SpentEarned[0]
            self.monthlyEarned = SpentEarned[1]
            return self.weeklySpent
        return self.monthlySpent

    def getYearlySpent(self) -> float:
        if not self.yearlySpent:
            SpentEarned: list = self.getExpenses_Budget(365)
            self.yearlySpent = SpentEarned[0]
            self.yearlyEarned = SpentEarned[1]
            return self.yearlySpent
        return self.yearlySpent

    def getWeeklyEarned(self) -> float:
        if not self.weeklyEarned:
            self.getWeeklySpent()
        return self.weeklyEarned

    def getMonthlyEarned(self) -> float:
        if not self.monthlyEarned:
            self.getMonthlySpent()
        return self.monthlyEarned

    def getYearlyEarned(self) -> float:
        if not self.yearlyEarned:
            self.getYearlySpent()
        return self.yearlyEarned

    # budget for the month or year is money earned * projected earnings

    def getExpenses_Budget(self, timeframe: int) -> list:
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

        projectedEarnings = self.getProjectedEarnings(timeframe)
        budget = projectedEarnings + budget
        return [currSpent, budget]

    def getProjectedEarnings(self, timeline: int) -> float:
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


class ClientIO(object):
    def __init__(self, bankInterface: BankInterface, csvInterface: CSVInterface):
        self.bankInterface: BankInterface = bankInterface
        self.csvInterface: CSVInterface = csvInterface

    def percentOfWeeklyBudgetSpent(self) -> float:
        weeklyBudget: float = self.csvInterface.getWeeklyEarned()
        return round(self.csvInterface.getWeeklySpent() / weeklyBudget * 100, 2)

    def percentOfMonthlyBudgetSpent(self) -> float:
        monthlyBudget: float = self.csvInterface.getMonthlyEarned()
        return round(self.csvInterface.getMonthlySpent() / monthlyBudget * 100, 2)

    def percentOfYearlyBudgetSpent(self) -> float:
        yearlyBudget: float = self.csvInterface.getYearlyEarned()
        return round(self.csvInterface.getYearlySpent() / yearlyBudget * 100, 2)

    def output(self):
        print("Money spent today: " + str(self.bankInterface.getDailySpent()))
        print(
            "Percent of weekly budget spent: " + str(self.percentOfWeeklyBudgetSpent())
        )
        print(
            "Percent of monthly budget spent: "
            + str(self.percentOfMonthlyBudgetSpent())
        )
        print(
            "Percent of yearly budget spent: " + str(self.percentOfYearlyBudgetSpent())
        )

    def sendEmail(self):
        pass


# TODO: set up EC2 instance
# TODO: set up cron job to run this script every day
# TODO: set up email service to send email to user


def populateCSV():
    csvWrite: csv = open("./src/data.csv", "w", newline="")
    csvWriter: csv.writer = csv.writer(csvWrite)
    csvWriter.writerow(["Date", "Amount Spent", "Daily Budget"])
    days = 15
    startDate: datetime = datetime.date(datetime.now() - timedelta(days=days))
    import random
    for i in range(1, days):
        csvWriter.writerow(
            [str(startDate + timedelta(days=i)), random.randint(20, 75), 58.88]
        )


#  populateCSV()


def __main__():
    bankInterface = BankInterface()
    csvInterface = CSVInterface(bankInterface)
    csvInterface.addDailySpent()
    csvInterface.getWeeklySpent()
    csvInterface.getMonthlySpent()
    csvInterface.getYearlySpent()

    clientIO: ClientIO = ClientIO(bankInterface, csvInterface)
    clientIO.output()


__main__()
