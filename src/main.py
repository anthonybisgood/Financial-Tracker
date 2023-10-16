from BankInterface import BankInterface
from CSVInterface import CSVInterface
from ClientIO import ClientIO
from MintConnection import MintConnection


# TODO: set up EC2 instance
# TODO: set up cron job to run this script every day

#  populateCSV()


def __main__():
    mintConn = MintConnection()
    mintConn.startMintConn()
    bankInterface = BankInterface(mintConn)
    csvInterface = CSVInterface(bankInterface)
    csvInterface.addDailySpent()
    mintConn.closeMintConn()
    clientIo = ClientIO(bankInterface, csvInterface)
    clientIo.sendText()
    

if __name__ == __main__():
    __main__
    