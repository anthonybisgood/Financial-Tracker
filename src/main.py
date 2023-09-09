import csv
from datetime import datetime, timedelta
from BankInterface import BankInterface
from CSVInterface import CSVInterface
from ClientIO import ClientIO



# TODO: set up EC2 instance
# TODO: set up cron job to run this script every day
# TODO: set up email service to send email to user
# TODO: set up link to bank account info


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


if __name__ == __main__():
    __main__
    
