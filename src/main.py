from typing import Tuple
from BankInterface import BankInterface
from ClientIO import ClientIO
import sqlite3
import subprocess
import os
import getLogger

DEV_MODE = 0
SUBSCRIPTIONS = 1

logger = getLogger.getLogger()


def __main__():
    logger.info("Starting program")
    logger.debug("Starting main.py")
    initializeDB(logger)
    dbConn, cursor = createDBConn(logger)
    bankInterface = BankInterface(logger, cursor)
    clientIO = ClientIO(logger, bankInterface)
    sendText(clientIO)
    dbConn.commit()
    cursor.close()
    dbConn.close()
    logger.debug("Closed database")
    logger.info("Program finished")


def sendText(clientIO: ClientIO):
    if DEV_MODE:
        logger.debug("In dev mode, not sending text")
        clientIO._genericMessage()
        return
    try:
        clientIO.sendText()
    except Exception as e:
        logger.exception("Error sending text message: %s", e)
        logger.error("Error sending text")


def createDBConn(logger) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    try:
        dbConn = sqlite3.connect("../data/budget.db")
        logger.debug("Opened database successfully")
        cursor = dbConn.cursor()
        return dbConn, cursor
    except Exception as e:
        logger.exception("Error opening database: %s", e)
        logger.fatal("Error opening database, exiting", exc_info=True)
        exit(0)


def initializeDB(logger):
    # if the db doesn't exist, run createDB.py
    logger.debug("Initializing database")
    createDBFile = "createDB.py"
    result = subprocess.run(["python3", createDBFile], capture_output=True)
    if result.returncode != 0:
        logger.info("Could not create database. Exiting.")
        logger.exception(result.stderr.decode("utf-8"))
        logger.error("Error running createDB.py")
        exit(0)
    else:
        logger.debug("createDB.py ran successfully")
    # add transactions to the db
    logger.info("Adding transactions to the database")
    addToDBFile = "addToDB.js"
    result = subprocess.run(["node", addToDBFile], capture_output=True)
    if result.returncode != 0:
        logger.exception(result.stderr.decode("utf-8"))
        exit(0)
    else:
        logger.debug("addToDB.js ran successfully")
    logger.info("Database initialized")


if __name__ == __main__():
    __main__
