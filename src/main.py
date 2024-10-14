from BankInterface import BankInterface
from ClientIO import ClientIO
import sqlite3
import subprocess
import os
import datetime


def __main__():
    print(datetime.datetime.now())
    initializeDB()
    dbConn = None
    cursor = None
    try:
        dbConn = sqlite3.connect("../data/budget.db")
        print("Opened database successfully")
        cursor = dbConn.cursor()
    except Exception as e:
        print("Error opening database:", e)
        exit(0)
    bankInterface = BankInterface(cursor)
    clientIO = ClientIO(bankInterface)
    clientIO.percentOfWeeklyBudgetSpent()
    clientIO.sendText()
    dbConn.commit()
    cursor.close()
    dbConn.close()


def initializeDB():
    # if the db doesn't exist, run createDB.py
    if not os.path.exists("../data/budget.db"):
        createDBFile = "createDB.py"
        result = subprocess.run(["python3", createDBFile], capture_output=True)
        if result.returncode != 0:
            print(result.stderr.decode("utf-8"))
            print("Error running createDB.py")
            exit(0)
        else:
            print("createDB.py ran successfully")
    # add transactions to the db
    addToDBFile = "addToDB.js"
    result = subprocess.run(["node", addToDBFile], capture_output=True)
    if result.returncode != 0:
        print("Error running addToDB.js")
        exit(0)
    else:
        print("addToDB.js ran successfully")


if __name__ == __main__():
    __main__
