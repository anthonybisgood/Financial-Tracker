const sqlite3 = require("sqlite3").verbose();

const db = new sqlite3.Database("./data/budget.db", (err) => {
  if (err) {
    console.error(err.message);
  } else {
    console.log("Connected to the budget database.");
  }
});

function selectAccounts() {
  db.all(`SELECT * FROM ACCOUNTS`, [], (err, rows) => {
    if (err) {
      console.error(err.message);
    }
    rows.forEach((row) => {
      console.log(row.accountID, row.accountType, row.accountName);
    });
  });
}

function selectTransactions() {
  db.all(`SELECT * FROM TRANSACTIONS ORDER BY date asc`, [], (err, rows) => {
    if (err) {
      console.error(err.message);
    }
    rows.forEach((row) => {
      console.log(
        row.transactionID,
        row.accountID,
        row.date,
        row.payee,
        row.amount
      );
    });
  });
}

function getCheckingTransactions() {
  db.all(
    "SELECT * FROM TRANSACTIONS WHERE accountID = '73af50de-b008-4a45-a7cf-f0240def1ebf' ORDER BY date asc",
    [],
    (err, rows) => {
      if (err) {
        console.error(err.message);
      } else
        rows.forEach((row) => {
          console.log(row);
        });
    }
  );
  console.log("Checking Transactions");
}
// selectTransactions();
selectAccounts();
getCheckingTransactions();

