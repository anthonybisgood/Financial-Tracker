from BankInterface import BankInterface
from ClientIO import ClientIO
from datetime import datetime, timedelta
import sqlite3
import subprocess



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
    clientIO = ClientIO(bankInterface)
    clientIO.sendText()
    dbConn.commit()
    cursor.close()
    dbConn.close()


if __name__ == __main__():
    __main__
