from BankInterface import BankInterface
from datetime import datetime, timedelta
import sqlite3
import subprocess

# TODO: set up EC2 instance
# TODO: set up cron job to run this script every day

#  populateCSV()


def __main__():
    addToDBFile = "src/addToDB.js"
    result = subprocess.run(["node", addToDBFile], capture_output=True)
    if result.returncode != 0:
        print("Error running addToDB.js")
        exit(0)
    else:
        print("addToDB.js ran successfully")
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
    
    day = datetime.date(datetime.now()) - timedelta(days=2)
    spend_on_day = 0
    spend_on_day = bankInterface.getSpentOnDay(day, creditAccounts)
    print(spend_on_day)
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
