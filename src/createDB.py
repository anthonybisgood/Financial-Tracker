# ERD: https://lucid.app/lucidchart/2fa548f9-1e73-48d5-bfa3-2e7f4907889f/edit?invitationId=inv_52e43567-b463-4274-8d68-6c7205cf3ea5&page=0_0#
import sqlite3
import getLogger

logger = getLogger.getLogger()

try:
    conn = sqlite3.connect("../data/budget.db")
    logger.debug("Opened database successfully")
except Exception as e:
    logger.debug("Error opening database:", e)
    exit(0)


def tableExists(tableName: str) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='"
        + tableName
        + "'"
    )
    if cursor.fetchone()[0] == 1:
        return True
    return False


cursor = conn.cursor()
create_transactions_table = """CREATE TABLE TRANSACTIONS (transactionID varchar(255) PRIMARY KEY, date date, amount DECIMAL(19, 4), payee varchar(255), accountID varchar(255));"""
create_accounts_table = """CREATE TABLE ACCOUNTS (accountID varchar(255) PRIMARY KEY, accountType varchar(255), accountName varchar(255));"""
create_pending_transactions_table = """CREATE TABLE PENDING_TRANSACTIONS (id int PRIMARY KEY,date date, amount DECIMAL(19, 4));"""
create_app_table = """CREATE TABLE APP_DATA (id INTEGER PRIMARY KEY AUTOINCREMENT, key varchar(255), value varchar(255));"""


def create_table(tableName: str, statement: str) -> None:
    if not tableExists(tableName):
        cursor.execute(statement)
        logger.debug(f"Created {tableName} table")


create_table("TRANSACTIONS", create_transactions_table)
create_table("ACCOUNTS", create_accounts_table)
create_table("PENDING_TRANSACTIONS", create_pending_transactions_table)
create_table("APP_DATA", create_app_table)


conn.commit()
cursor.close()
conn.close()
logger.debug("Closed database connection")
logger.info("Created database")
