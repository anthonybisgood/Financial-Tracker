from BankInterface import BankInterface
from ClientIO import ClientIO
import sqlite3
import subprocess
import os


def __main__():
    initializeDB()
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
    # clientIO.sendText()
    dbConn.commit()
    cursor.close()
    dbConn.close()


def initializeDB():
    # if the db doesnt exist, run createDB.py
    if not os.path.exists("./data/budget.db"):
        createDBFile = "src/createDB.py"
        result = subprocess.run(["python", createDBFile], capture_output=True)
        if result.returncode != 0:
            print("Error running createDB.py")
            exit(0)
        else:
            print("createDB.py ran successfully")
    # add transacaions to the db
    addToDBFile = "src/addToDB.js"
    result = subprocess.run(["node", addToDBFile], capture_output=True)
    if result.returncode != 0:
        print("Error running addToDB.js")
        exit(0)
    else:
        print("addToDB.js ran successfully")


if __name__ == __main__():
    __main__
