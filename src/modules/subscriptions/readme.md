# Subscription module

This module is in charge of tracking the subscriptions of the users based on their YNAB transactions.

## Issues

Subscription payments are not always on the same day of the month, or even the same price each month. Subscriptions can change prices and dates from month to month. This makes it difficult to track subscriptions. There are also different types of subscriptions, such as yearly, monthly, and weekly subscriptions.

### Solution

What transactions qualify a "Subscription"?

1. Transactions that are the same amount each period with a `3%` deviation in cost.
   1. This is to account for small changes in subscription price due to small changes in the way the subscription is calculated.
2. Subscriptions are payed once per their respective period. (i.e. monthly subscriptions are paid once a month, yearly subscriptions are paid once a year, etc.)
3. Transactions are recurring.

## Implementation

Only 2 types of periods are supported: `monthly` and `yearly`. This is because most subscriptions are either monthly or yearly.
