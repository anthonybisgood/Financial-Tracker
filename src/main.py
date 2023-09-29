import csv
from datetime import datetime, timedelta
import time
from BankInterface import BankInterface
from CSVInterface import CSVInterface
from ClientIO import ClientIO
from MintConnection import MintConnection


# TODO: set up EC2 instance
# TODO: set up cron job to run this script every day

#  populateCSV()


def __main__():
    mintConn = MintConnection()
    mintConn.startMintConn()
    bankInterface = BankInterface(mintConn)
    csvInterface = CSVInterface(bankInterface)
    csvInterface.addDailySpent()
    clientIo = ClientIO(bankInterface, csvInterface)
    clientIo.sendText()

if __name__ == __main__():
    __main__
    


# def populateCSV():
#     csvWrite: csv = open("./src/data.csv", "w", newline="")
#     csvWriter: csv.writer = csv.writer(csvWrite)
#     csvWriter.writerow(["Date", "Amount Spent", "Daily Budget"])
#     days = 15
#     startDate: datetime = datetime.date(datetime.now() - timedelta(days=days))
#     import random

#     for i in range(1, days):
#         csvWriter.writerow(
#             [str(startDate + timedelta(days=i)), random.randint(20, 75), 58.88]
#         )
