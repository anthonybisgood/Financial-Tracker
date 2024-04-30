// Description: This script adds the accounts from the YNAB API to the database.
const path = require("path");
const ynab = require("ynab");
require("dotenv").config(path.resolve(__dirname, ".env"));
const accessToken = process.env.YNAB_API_KEY;
const ynabAPI = new ynab.API(accessToken);
const sqlite3 = require("sqlite3").verbose();
const today = new Date();
const todyasDate =
  today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();

const db = new sqlite3.Database("./data/budget.db", (err) => {
  if (err) {
    console.error(err.message);
  } else {
    console.log("Connected to the budget database.");
  }
});

async function getBudgetID() {
  const budgetsResponse = await ynabAPI.budgets.getBudgets();
  const budgets = budgetsResponse.data.budgets;
  const budgetId = budgets[0].id;
  return budgetId;
}

/**
 * @param {*} budgetID
 * @returns a map of accountID:[accountType, accountName]
 */
async function getAccounts(budgetID) {
  // make delta request to get all accounts
  const accounts = await ynabAPI.accounts.getAccounts(budgetID);
  const accountMap = new Map();
  for (let account of accounts.data.accounts) {
    const accountType = account.type;
    accountMap.set(account.id, [accountType, account.name]);
  }
  return accountMap;
}

function addAccountsToDB(accountsMap) {
  for (let [accountID, accountInfo] of accountsMap) {
    const accountType = accountInfo[0];
    const accountName = accountInfo[1];
    db.run(
      `INSERT OR IGNORE INTO ACCOUNTS(accountID, accountType, accountName) VALUES(?, ?, ?)`,
      [accountID, accountType, accountName],
      (err) => {
        if (err) {
          console.error(err.message);
        }
      }
    );
  }
}

/**
 *
 * @param {string} accountType "creditCard" or "checking" or "savings" or "otherAsset"
 * @returns a list of accountIDs that match the accountType
 */
async function getAccountIDs(accountType) {
  return new Promise((resolve, reject) => {
    const accountIDs = [];
    db.all(
      `SELECT accountID FROM ACCOUNTS WHERE accountType = ?`,
      [accountType],
      (err, rows) => {
        if (err) {
          console.error(err.message);
          reject(err);
        }
        rows.forEach((row) => {
          accountIDs.push(row.accountID);
        });
        resolve(accountIDs);
      }
    );
  });
}

async function postTransactionsToDB(budgetId) {
  const accountIDs = await getAccountIDs("creditCard");
  for (let accountID of accountIDs) {
    const transactions = await getTransactions(budgetId, accountID);
    for (let transaction of transactions) {
      addTransactionToDB(accountID, transaction);
    }
  }
}

async function getTransactions(budgetId, accountID) {
  try {
    const transactionsResponse =
      await ynabAPI.transactions.getTransactionsByAccount(budgetId, accountID);
    const transactions = transactionsResponse.data.transactions;
    return transactions;
  } catch (err) {
    console.error("Transaction error:", err.message);
  }
}

async function addTransactionToDB(accountID, transaction) {
  const transactionID = transaction.id;
  const date = transaction.date;
  const amount = transaction.amount;
  const payee = transaction.payee_name;
  db.run(
    `INSERT OR IGNORE INTO TRANSACTIONS(transactionID, accountID, date, payee, amount) VALUES(?, ?, ?, ?, ?)`,
    [transactionID, accountID, date, payee, -(amount/1000)],
    (err) => {
      if (err) {
        console.error(err.message);
      }
    }
  );
}

async function main() {
  const budgetId = await getBudgetID();
  const accountsMap = await getAccounts(budgetId);

  addAccountsToDB(accountsMap);
  await postTransactionsToDB(budgetId);
  closeDB();
}

main();

function closeDB() {
  db.close((err) => {
    if (err) {
      console.error(err.message);
    } else {
      console.log("Closed the database connection.");
    }
  });
}
