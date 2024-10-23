from BankInterface import BankInterface
from ClientIO import ClientIO
import sqlite3
import subprocess
import os
import datetime
import logging


def __main__():
    logging.basicConfig(
        filename="../logs/log.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
    )
    logger = logging.getLogger()
    logger.debug("Starting main.py")
    initializeDB(logger)
    dbConn = None
    cursor = None
    try:
        dbConn = sqlite3.connect("../data/budget.db")
        logger.debug("Opened database successfully")
        cursor = dbConn.cursor()
    except Exception as e:
        logger.exception("Error opening database: %s", e)
        exit(0)
    bankInterface = BankInterface(cursor)
    clientIO = ClientIO(bankInterface)
    clientIO.percentOfWeeklyBudgetSpent()
    clientIO.sendText()
    dbConn.commit()
    cursor.close()
    dbConn.close()


def initializeDB(logger):
    # if the db doesn't exist, run createDB.py
    if not os.path.exists("../data/budget.db"):
        logger.debug("Initializing database")
        createDBFile = "createDB.py"
        result = subprocess.run(["python3", createDBFile], capture_output=True)
        if result.returncode != 0:
            logger.exception(result.stderr.decode("utf-8"))
            logger.error("Error running createDB.py")
            exit(0)
        else:
            logger.debug("createDB.py ran successfully")
    # add transactions to the db
    logger.debug("Adding transactions to the database")
    addToDBFile = "addToDB.js"
    result = subprocess.run(["node", addToDBFile], capture_output=True)
    if result.returncode != 0:
        logger.error(result.stderr.decode("utf-8"))
        exit(0)
    else:
        logger.debug("addToDB.js ran successfully")
    logger.debug("Database initialized")


if __name__ == __main__():

    __main__
