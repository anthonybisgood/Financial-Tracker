import sqlite3

try:
    conn = sqlite3.connect('transactions.db')
    print("Opened database successfully")
except:
    print("Error opening database")
    exit(0)

tables = ["TRANSACTIONS", "ACCOUNTS"]

conn.close()