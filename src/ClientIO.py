from BankInterface import BankInterface
from CSVInterface import CSVInterface
import os
from twilio.rest import Client


class ClientIO(object):
    def __init__(self, bankInterface: BankInterface, csvInterface: CSVInterface):
        self.bankInterface: BankInterface = bankInterface
        self.csvInterface: CSVInterface = csvInterface

    def percentOfWeeklyBudgetSpent(self) -> float:
        weeklyBudget: float = self.csvInterface.getWeeklyEarned()
        return round(self.csvInterface.getWeeklySpent() / weeklyBudget * 100, 2)

    def percentOfMonthlyBudgetSpent(self) -> float:
        monthlyBudget: float = self.csvInterface.getMonthlyEarned()
        return round(self.csvInterface.getMonthlySpent() / monthlyBudget * 100, 2)

    def percentOfYearlyBudgetSpent(self) -> float:
        yearlyBudget: float = self.csvInterface.getYearlyEarned()
        return round(self.csvInterface.getYearlySpent() / yearlyBudget * 100, 2)

    def output(self):
        print("Money spent today: " + str(self.bankInterface.getDailySpent()))
        print(
            "Percent of weekly budget spent: " + str(self.percentOfWeeklyBudgetSpent())
        )
        print(
            "Percent of monthly budget spent: "
            + str(self.percentOfMonthlyBudgetSpent())
        )
        print(
            "Percent of yearly budget spent: " + str(self.percentOfYearlyBudgetSpent())
        )

    def sendText(self):
        account_sid = os.getenv("TWLIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)
        message = client.messages.create(body="", from_="", to_="+15204440142")
