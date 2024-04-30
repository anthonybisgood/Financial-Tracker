from BankInterface import BankInterface
from datetime import datetime, timedelta
import sqlite3


# TODO: set up EC2 instance
# TODO: set up cron job to run this script every day

#  populateCSV()


def __main__():
    dbConn = None
    cursor = None
    try:
        dbConn = sqlite3.connect("./data/budget.db")
        print("Opened database successfully")
        cursor = dbConn.cursor()
    except:
        print("Error opening database")
        exit(0) 
    
    bankInterface = BankInterface(cursor)
    creditAccounts = bankInterface._getAccountIDs("creditCard")
    print(creditAccounts)
    
    bankInterface.getSpentOnDay(datetime.date(datetime.now()) - timedelta(days=2), creditAccounts[0])
    dbConn.commit()
    cursor.close()
    dbConn.close()
    
    # yesterdaysDate: datetime = datetime.date(datetime.now()) - timedelta(days=1)
    # csvInterface.addDailySpent(yesterdaysDate)
    # mintConn.closeMintConn()
    # clientIo = ClientIO(bankInterface, csvInterface)
    # clientIo.sendText()


if __name__ == __main__():
    __main__
