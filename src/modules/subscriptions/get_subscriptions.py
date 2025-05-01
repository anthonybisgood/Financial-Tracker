from datetime import datetime, timedelta
import sqlite3
import sys
import os

# from .. import getLogger

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
        AND avg_interval_days BETWEEN 365 AND 367 -- Adjust for period (yearly here with ±5 days)
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

# logger = getLogger.getLogger()


# def main():
#     dbconn = get_dbConn()
#     cursor = dbconn.cursor()
#     monthly_subscriptions = get_monthly_subscriptions(cursor)
#     yearly_subscriptions = get_yearly_subscriptions(cursor)
#     get_subscription_total(yearly_subscriptions)
#     get_subscription_total(monthly_subscriptions)
#     yearly_subscriptions = get_yearly_subscriptions(cursor)
#     get_subscription_total(yearly_subscriptions)


# def get_dbConn():
#     return sqlite3.connect("/app/data/budget.db")


# def get_monthly_subscriptions(cursor):
#     monthly_subscriptions = cursor.execute(MONTHLY_QUERY)
#     return monthly_subscriptions


# def get_yearly_subscriptions(cursor):
#     yearly_subscriptions = cursor.execute(YEARLY_QUERY)
#     return yearly_subscriptions


# def get_subscription_total(subscriptions):
#     total = 0
#     for subscription in subscriptions:
#         print(subscription)
#     return total


# if __name__ == "__main__":
#     main()


import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from collections import defaultdict


def get_subscriptions(db_path):
    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Get all transactions sorted by payee and date
    query = """
    SELECT t.TransactionID, t.AccountID, t.date, t.payee, t.Amount, a.AccountName, a.AccountType
    FROM Transactions t
    JOIN Accounts a ON t.AccountID = a.AccountID
    ORDER BY t.payee, t.date
    """

    # Load into pandas for easier manipulation
    df = pd.read_sql_query(query, conn)

    # Convert date strings to datetime objects
    df["date"] = pd.to_datetime(df["date"])

    # Normalize payee names (remove special characters, convert to lowercase)
    df["normalized_payee"] = df["payee"].apply(
        lambda x: re.sub(r"[^a-zA-Z0-9]", "", x).lower()
    )

    # Group potentially similar payees
    similar_payees = defaultdict(list)

    # For each unique normalized payee
    for payee in df["normalized_payee"].unique():
        # Find similar payees (simple approach: if one is substring of another)
        for other_payee in df["normalized_payee"].unique():
            if payee != other_payee and (payee in other_payee or other_payee in payee):
                # Store mapping of similar payees
                similar_payees[payee].append(other_payee)

    # Identify possible subscriptions
    subscriptions = []

    # Group by normalized payee
    for payee, group in df.groupby("normalized_payee"):
        # Skip if only one transaction (need at least two to identify a pattern)
        if len(group) < 2:
            continue

        # Check related payees too
        related_transactions = df[
            df["normalized_payee"].isin([payee] + similar_payees[payee])
        ]

        # Sort by date
        related_transactions = related_transactions.sort_values("date")

        # Calculate days between transactions
        days_diff = []
        for i in range(1, len(related_transactions)):
            days = (
                related_transactions.iloc[i]["date"]
                - related_transactions.iloc[i - 1]["date"]
            ).days
            days_diff.append(days)

        # Skip if we don't have enough data points
        if not days_diff:
            continue

        # Check for monthly patterns (25-35 days)
        if any(25 <= d <= 35 for d in days_diff):
            subscription_type = "Monthly"
        # Check for yearly patterns (350-380 days)
        elif any(350 <= d <= 380 for d in days_diff):
            subscription_type = "Yearly"
        else:
            # Not a subscription or irregular
            continue

        # Calculate average amount and variation
        amounts = related_transactions["amount"].values
        avg_amount = np.mean(amounts)
        max_variation = max(abs(a - avg_amount) for a in amounts)

        # If amount variation is too large, might not be a subscription
        if (
            max_variation / avg_amount > 0.1 and max_variation > 5
        ):  # 20% variation and > $5 change
            continue

        # Add to subscriptions
        original_payees = related_transactions["payee"].unique()

        subscriptions.append(
            {
                "subscription_type": subscription_type,
                "payee_variations": list(original_payees),
                "average_amount": round(avg_amount, 2),
                "last_payment_date": related_transactions["date"]
                .max()
                .strftime("%Y-%m-%d"),
                "next_expected_date": (
                    related_transactions["date"].max()
                    + timedelta(days=30 if subscription_type == "Monthly" else 365)
                ).strftime("%Y-%m-%d"),
                "transaction_count": len(related_transactions),
            }
        )

    conn.close()
    return subscriptions


# Example usage
if __name__ == "__main__":
    subscriptions = get_subscriptions("../../../data/budget.db")

    print(f"Found {len(subscriptions)} subscriptions:")
    for i, sub in enumerate(subscriptions, 1):
        print(
            f"\n{i}. {' / '.join(sub['payee_variations'])} - {sub['subscription_type']}"
        )
        print(f"   Amount: ${sub['average_amount']:.2f}")
        print(f"   Last payment: {sub['last_payment_date']}")
        print(f"   Next expected: {sub['next_expected_date']}")
        print(f"   Based on {sub['transaction_count']} transactions")
