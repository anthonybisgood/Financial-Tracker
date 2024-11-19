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

### Installation

1. **Clone the Repository**

   Clone the project repository from GitHub:

   ```bash
   git clone https://github.com/anthonybisgood/financial-tracker.git
   ```

2. **Set Up Environment Variables**

    Create a .env file in the root directory and add the following variables:
    - EMAIL=<your-email@example.com>
    - APP_PASS=your-email-app-password
      - <https://support.google.com/accounts/answer/185833?hl=en>
    - PHONE_NUM=your-phone-number
    - YNAB_API_KEY=your-ynab-api-key

3. **Run with build_run.sh**

### FAQ & Info

1. Why don't I receive emails about my budget:
   - The EMAIL must have 2FA disabled and an app password generated for the APP_PASS variable.
2. Budgets info is sent every day at 6am.
3. Only useable over 1 budget in YNAB. Added debit accounts count as money in and credit accounts as money out.
