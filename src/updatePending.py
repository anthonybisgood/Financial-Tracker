# addPending.py
# created to add pending transactions at end-of-day to the database for next-days posting
# supposed to be ran at 12:00AM every day along
from MintConnection import MintConnection
from BankInterface import BankInterface
import pandas as pd
import sqlite3

def getTodaysTransactions() -> pd.DataFrame:
    accounts = bankInterface._getCreditAccounts()
    transactions = pd.DataFrame()
    for account in accounts:
        transaction = bankInterface._get_account_transactions(account)
        transactions = pd.concat([transactions, transaction]).sort_values(by="date")
    return transactions

def getDBConnection() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect("./data/transactions.db")
        print("Opened database successfully")
    except:
        print("Error opening database")
        exit(0)
    return conn

credit_transactions = getTodaysTransactions()
pending_transactions: pd.DataFrame = credit_transactions.loc[
    credit_transactions["isPending"] == True
]
pending_transactions.drop_duplicates(subset=["id"], inplace=True)
pending_transactions = pending_transactions[
    pending_transactions["description"].apply(
        lambda x: isinstance(x, str) and "Payment" not in x
    )
]
pending_transactions = pending_transactions[["id", "date", "amount"]]
conn = getDBConnection()
cursor = conn.cursor()
cursor.execute("DELETE FROM PENDING_TRANSACTIONS")
pending_transactions.to_sql(
    "PENDING_TRANSACTIONS", conn, if_exists="append", index=False
)
cursor.execute("SELECT * FROM PENDING_TRANSACTIONS")
x = cursor.fetchall()
cursor.close()
conn.close()
mintConn.closeMintConn()
