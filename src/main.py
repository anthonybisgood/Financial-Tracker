import csv
from datetime import datetime, timedelta


class BankInterface(object):
    def __init__(self):
        # create link to bank account and login, get account info
        self.dailySpent = None
        pass

    def getDailySpent(self) -> float:
        # So we only fetch once
        if not self.dailySpent:
            self.dailySpent = self.fetchDailySpent()
            return self.dailySpent
        return self.dailySpent

    def fetchDailySpent(self):
        # Get daily spent from bank account
        return 60.0

    def getLastPaycheck(self) -> float:
        # Do This later, This would be the biweekly paycheck amount
        return 1800

    def weeklyBudget(self) -> float:
        return self.getLastPaycheck() / 4

    def getMonthlyBudget(self) -> float:
        return self.getLastPaycheck()


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
        csvWrite: csv = open("./data.csv", "a", newline="")
        amountSpent: float = self.bankInterface.getDailySpent()
        csvWriter: csv.writer = csv.writer(csvWrite)
        dailyBudget: float = self.bankInterface.weeklyBudget() / 7
        csvWriter.writerow([str(self.todaysDate), str(amountSpent), dailyBudget])
        csvWrite.close()

    def getWeeklySpent(self) -> float:
        if not self.weeklySpent:
            SpentEarned: list = self.getSpentEarnedFromXDaysAgo(7)
            self.weeklySpent = SpentEarned[0]
            self.weeklyEarned = SpentEarned[1]
            return self.weeklySpent
        return self.weeklySpent

    def getMonthlySpent(self) -> float:
        if not self.monthlySpent:
            SpentEarned: list = self.getSpentEarnedFromXDaysAgo(30)
            self.monthlySpent = SpentEarned[0]
            self.monthlyEarned = SpentEarned[1]
            return self.weeklySpent
        return self.monthlySpent

    def getYearlySpent(self) -> float:
        if not self.yearlySpent:
            SpentEarned: list = self.getSpentEarnedFromXDaysAgo(365)
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

    def getSpentEarnedFromXDaysAgo(self, daysAgo: int) -> list:
        """Gets the amount spent from x days ago (exclusive) to today (inclusive)

        Args:
            daysAgo (int): The number of days ago to start counting from

        Returns:
            float: The amount spent from x days ago to today
        """
        currSpent: float = 0
        currEarned: float = 0
        daysAgoDate: datetime = self.todaysDate - timedelta(days=daysAgo)
        datesFromDaysAgo: list = []
        for i in range(1, daysAgo + 1):
            datesFromDaysAgo.append(str(daysAgoDate + timedelta(days=i)))
        csvRead: csv = open("./data.csv", "r")
        csvReader: csv.reader = csv.reader(csvRead)
        for row in csvReader:
            if row and row[0] in datesFromDaysAgo:
                currSpent += float(row[1])
                currEarned += float(row[2])
        csvRead.close()
        return [currSpent, currEarned]


class ClientIO(object):
    def __init__(self, bankInterface: BankInterface, csvInterface: CSVInterface):
        self.bankInterface: BankInterface = bankInterface
        self.csvInterface: CSVInterface = csvInterface

    def percentOfWeeklyBudgetSpent(self) -> float:
        weeklyBudget: float = self.bankInterface.weeklyBudget()
        return self.csvInterface.getWeeklySpent() / weeklyBudget * 100

    def percentOfMonthlyBudgetSpent(self) -> float:
        monthlyBudget: float = self.bankInterface.getMonthlyBudget()
        return self.csvInterface.getMonthlySpent() / monthlyBudget * 100

    def percentOfYearlyBudgetSpent(self) -> float:
        yearlyBudget: float = self.bankInterface.getMonthlyBudget() * 12
        return self.csvInterface.getYearlySpent() / yearlyBudget * 100

    def getMoneySpentToday(self) -> float:
        return self.bankInterface.getDailySpent()


def __main__():
    bankInterface = BankInterface()
    csvInterface = CSVInterface(bankInterface)
    csvInterface.addDailySpent()
    clientIO: ClientIO = ClientIO(bankInterface, csvInterface)
    clientIO.getMoneySpentToday()
    print(csvInterface.getMonthlyEarned())


__main__()
