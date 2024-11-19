from datetime import datetime, timedelta
import sqlite3
import sys
import os

from src.modules import getLogger

MONTHLY_QUERY = """
WITH TransactionGroups AS (
    SELECT 
        t.AccountID,
        t.payee,
        t.Amount,
        t.date,
        LAG(t.date) OVER (PARTITION BY t.AccountID, t.payee ORDER BY t.date) AS previous_transaction_date,
        ROUND(ABS((t.Amount - LAG(t.Amount) OVER (PARTITION BY t.AccountID, t.payee ORDER BY t.date)) / t.Amount), 4) AS amount_deviation
    FROM 
        Transactions t
),
PotentialSubscriptions AS (
    SELECT 
        tg.AccountID,
        tg.payee,
        COUNT(*) AS occurrences,
        ROUND(AVG(tg.Amount), 2) AS average_subscription_cost, -- Average cost of subscription
        AVG(JULIANDAY(tg.date) - JULIANDAY(tg.previous_transaction_date)) AS avg_interval_days,
        MIN(tg.date) AS first_transaction,
        MAX(tg.date) AS last_transaction
    FROM 
        TransactionGroups tg
    WHERE 
        tg.amount_deviation <= 0.03 -- Allowing a 5% deviation
        AND tg.previous_transaction_date IS NOT NULL
    GROUP BY 
        tg.AccountID, tg.payee
    HAVING 
        COUNT(*) >= 2 -- At least two transactions to consider recurring
        AND avg_interval_days BETWEEN 28 AND 31 -- Adjust for period (monthly here)
)
SELECT 
    ps.AccountID,
    a.AccountName,
    a.AccountType,
    ps.average_subscription_cost,
    ps.payee,
    ps.occurrences,
    ps.avg_interval_days,
    ps.first_transaction,
    ps.last_transaction
FROM 
    PotentialSubscriptions ps
JOIN 
    Accounts a ON ps.AccountID = a.AccountID;
"""

YEARLY_QUERY = """
WITH TransactionGroups AS (
    SELECT 
        t.AccountID,
        t.payee,
        t.Amount,
        t.date,
        LAG(t.date) OVER (PARTITION BY t.AccountID, t.payee ORDER BY t.date) AS previous_transaction_date,
        ROUND(ABS((t.Amount - LAG(t.Amount) OVER (PARTITION BY t.AccountID, t.payee ORDER BY t.date)) / t.Amount), 4) AS amount_deviation
    FROM 
        Transactions t
),
PotentialSubscriptions AS (
    SELECT 
        tg.AccountID,
        tg.payee,
        tg.amount,
        COUNT(*) AS occurrences,
        AVG(JULIANDAY(tg.date) - JULIANDAY(tg.previous_transaction_date)) AS avg_interval_days,
        MIN(tg.date) AS first_transaction,
        MAX(tg.date) AS last_transaction
    FROM 
        TransactionGroups tg
    WHERE 
        tg.amount_deviation <= 0.03 -- Allowing a 3% deviation
        AND tg.previous_transaction_date IS NOT NULL
    GROUP BY 
        tg.AccountID, tg.payee
    HAVING 
        COUNT(*) >= 2 -- At least two transactions to consider recurring
        AND avg_interval_days BETWEEN 365 AND 367 -- Adjust for period (monthly here)
)
SELECT 
    ps.AccountID,
    a.AccountName,
    a.AccountType,
    ps.amount,
    ps.payee,
    ps.occurrences,
    ps.avg_interval_days,
    ps.first_transaction,
    ps.last_transaction
FROM 
    PotentialSubscriptions ps
JOIN 
    Accounts a ON ps.AccountID = a.AccountID;
"""

logger = getLogger.getLogger()


def main():
    dbconn = get_dbConn()
    cursor = dbconn.cursor()
    monthly_subscriptions = get_monthly_subscriptions(cursor)
    get_subscription_total(monthly_subscriptions)


def get_dbConn():
    return sqlite3.connect("../data/budget.db")


def get_monthly_subscriptions(cursor):
    monthly_subscriptions = cursor.execute(MONTHLY_QUERY)
    return monthly_subscriptions


def get_yearly_subscriptions(cursor):
    yearly_subscriptions = cursor.execute(YEARLY_QUERY)
    return yearly_subscriptions


def get_subscription_total(subscriptions):
    total = 0
    for subscription in subscriptions:
        print(subscription)
    return total


if __name__ == "__main__":
    main()
