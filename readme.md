# Financial Tracker

This project is a financial tracking application that integrates with the YNAB API to manage budgets, track spending, and send notifications about budget status via email and text.

## Features

- **Database Management**: Uses SQLite to store transaction and account data.
- **API Integration**: Integrates with the YNAB API to fetch account and transaction data.
- **Budget Tracking**: Calculates and tracks weekly, monthly, and yearly spending against budgets.
- **Notification System**: Sends notifications about budget usage via email and SMS.

## Getting Started

### Prerequisites

- Docker
- An account with YNAB and a valid YNAB API key.
- A `.env` file in the root directory with the following variables:
    - EMAIL=your-email@example.com
    - APP_PASS=your-email-app-password
    - PHONE_NUM=your-phone-number
    - YNAB_API_KEY=your-ynab-api-key
