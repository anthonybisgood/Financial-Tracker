import os
import datetime as dt
import mintapi
from dotenv import load_dotenv
from pathlib import Path

class BankInterface(object):
    def __init__(self):
        # create link to bank account and login, get account info
        self.dailySpent = None
        self.lastPaycheck = None
        pass

    def getDailySpent(self) -> float:
        # So we only fetch once
        if not self.dailySpent:
            self.dailySpent = self.fetchDailySpent()
            return self.dailySpent
        return self.dailySpent

    def fetchDailySpent(self):
        # Get daily spent from bank account
        return 50.0

    def getLastPaycheck(self) -> float:
        if not self.lastPaycheck:
            self.lastPaycheck = self.fetchLastPaycheck()
            return self.lastPaycheck
        # Do This later, This would be the biweekly paycheck amount
        return self.lastPaycheck

    def fetchLastPaycheck(self):
        # Get last paycheck from bank account
        return 1648.55

class BankConnection(object):
    def __init__(self):
        load_dotenv()
        
        
    
def main():
    x = BankConnection()

main()