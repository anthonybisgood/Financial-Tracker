from BankInterface import BankInterface
from CSVInterface import CSVInterface
from MintConnection import MintConnection
from datetime import datetime, timedelta



with open("./data/data.csv", "r") as csv:
    data = csv.readlines()
    lastRow = data[-1]
    csv.close()
date = lastRow.split(",")[0]
start_date = datetime.strptime(date, "%Y-%m-%d").date() + timedelta(days=1)
end_date = datetime.date(datetime.now()) - timedelta(days=1)

date_list = []
current_date = start_date
while current_date < end_date:
    date_list.append(current_date)
    current_date += timedelta(days=1)
mintConn = MintConnection()
mintConn.startMintConn()
bankInterface = BankInterface(mintConn)
csvInterface = CSVInterface(bankInterface)    
for date in date_list:
    csvInterface.addDailySpent(date)