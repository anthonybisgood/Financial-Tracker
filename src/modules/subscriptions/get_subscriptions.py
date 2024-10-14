from datetime import datetime, timedelta
import sqlite3

MONTHLY_QUERY = """
    SELECT 
        t.AccountID,
        t.payee,
        t.Amount,
        t.date,
        LAG(t.date) OVER (PARTITION BY t.AccountID, t.payee ORDER BY t.date) AS previous_transaction_date,
        ROUND(ABS((t.Amount - LAG(t.Amount) OVER (PARTITION BY t.AccountID, t.payee ORDER BY t.date)) / t.Amount), 4) AS amount_deviation
    FROM 
        Transactions t
"""

def main():
    dbconn = get_dbConn()
    cursor = dbconn.cursor()
    subscriptions = get_subscriptions(cursor)

def get_dbConn():
    return sqlite3.connect("../../../data/budget.db")


def get_subscriptions(cursor):

    cursor.execute(MONTHLY_QUERY)
    subscriptions = cursor.fetchall()
    print(subscriptions)
    return subscriptions

# def get_monthly_subscriptions(cursor):

#     return monthly_subscriptions


# def get_yearly_subscriptions(cursor):

#     return yearly_subscriptions

if __name__ == "__main__":
    main()
