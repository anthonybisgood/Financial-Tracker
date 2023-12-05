# addPending.py
# created to add pending transactions at end-of-day to the database for next-days posting
from MintConnection import MintConnection
from BankInterface import BankInterface
import pandas as pd
import sqlite3

mintConn = MintConnection()
mintConn.startMintConn()
bankInterface = BankInterface(mintConn)


def getTransactions() -> pd.DataFrame:
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


credit_transactions = getTransactions()
credit_transactions.to_csv("./data/credit_transactions.csv")
pending_transactions = credit_transactions.loc[credit_transactions["isPending"] == True]
pending_transactions.drop_duplicates(subset=["id"], inplace=True)
pending_transactions = pending_transactions[
    pending_transactions["description"].apply(
        lambda x: isinstance(x, str) and "Payment" not in x
    )
]
dropped_columns = [
    "type",
    "metaData",
    "accountId",
    "transactionURN",
    "accountRef",
    "description",
    "category",
    "currency",
    "status",
    "matchState",
    "fiData",
    "isReviewed",
    "merchantId",
    "transactionType",
    "etag",
    "isExpense",
    "isPending",
    "discretionaryType",
    "isLinkedToRule",
    "transactionReviewState",
]
pending_transactions.drop(dropped_columns, axis=1, inplace=True)
print(pending_transactions)
conn = getDBConnection()
pending_transactions.to_sql("PENDING_TRANSACTIONS", conn, if_exists="append")

cursor = conn.cursor()
cursor.execute("SELECT * FROM PENDING_TRANSACTIONS")
x = cursor.fetchall()
print(x)

cursor.close()
conn.close()
# add pending_transactions to database table "pending_transactions"
# pending_transactions.to_sql("PENDING_TRANSACTIONS", conn, if_exists="append")
