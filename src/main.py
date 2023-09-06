import csv
from datetime import datetime, timedelta
from BankInterface import BankInterface
from CSVInterface import CSVInterface

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
# TODO: set up link to bank account


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
