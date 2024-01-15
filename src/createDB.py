import sqlite3

try:
    conn = sqlite3.connect("./data/transactions.db")
    print("Opened database successfully")
except:
    print("Error opening database")
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
create_transactions_table = """CREATE TABLE TRANSACTIONS (id int PRIMARY KEY, date date, amount DECIMAL(19, 4), description varchar(255), accountID int);"""
create_accounts_table = (
    """CREATE TABLE ACCOUNTS (id int PRIMARY KEY, bankAccountType varchar(255));"""
)
create_pending_transactions_table = """CREATE TABLE PENDING_TRANSACTIONS (id int PRIMARY KEY,date date, amount DECIMAL(19, 4));"""
# cursor.execute("DELETE FROM PENDING_TRANSACTIONS")
if not tableExists("TRANSACTIONS"):
    cursor.execute(create_transactions_table)
if not tableExists("ACCOUNTS"):
    cursor.execute(create_accounts_table)
if not tableExists("PENDING_TRANSACTIONS"):
    cursor.execute(create_pending_transactions_table)

conn.commit()
cursor.close()
conn.close()
