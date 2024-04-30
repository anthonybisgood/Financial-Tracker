from BankInterface import BankInterface
import os
import smtplib
from dotenv import load_dotenv
from datetime import datetime, timedelta

class ClientIO(object):

    def __init__(self, bankInterface: BankInterface, csvInterface: CSVInterface):
        self.bankInterface: BankInterface = bankInterface
        self.csvInterface: CSVInterface = csvInterface
        self.yesterdaysDate: datetime = datetime.date(datetime.now()) - timedelta(
            days=1
        )

    def percentOfWeeklyBudgetSpent(self) -> float:
        weeklyBudget: float = self.csvInterface.getWeeklyEarned()
        return round(self.csvInterface.getWeeklySpent() / weeklyBudget * 100, 2)

    def percentOfMonthlyBudgetSpent(self) -> float:
        monthlyBudget: float = self.csvInterface.getMonthlyEarned()
        return round(self.csvInterface.getMonthlySpent() / monthlyBudget * 100, 2)

    def percentOfYearlyBudgetSpent(self) -> float:
        yearlyBudget: float = self.csvInterface.getYearlyEarned()
        return round(self.csvInterface.getYearlySpent() / yearlyBudget * 100, 2)

    def _genericMessage(self) -> str:
        res = "\nSpent yesterday: ${}".format(str(self.bankInterface.getSpentYesterday()))
        res += "\nPercent of weekly budget spent:\n{}%".format(
            str(self.percentOfWeeklyBudgetSpent())
        )
        res += "\nPercent of monthly budget spent:\n{}%".format(
            str(self.percentOfMonthlyBudgetSpent())
        )
        res += "\r\n\r\n\r\n"
        return res

    def _firstOfTheMonthMessage(self) -> str:
        res = "Spent this month: ${}".format(str(self.csvInterface.getMonthlyEarned()))
        res += "\nPercent of yearly budget spent:\n{}%".format(
            str(self.percentOfYearlyBudgetSpent())
        )
        res += "\n"
        return res
    
    def getEmailServer(self):
        load_dotenv()
        email = str(os.getenv("EMAIL"))
        pas = str(os.getenv("EMAIL_PASS"))
        smtp = "smtp.gmail.com"
        port = 587
        server = smtplib.SMTP(smtp, port)
        server.starttls()
        server.login(email, pas)
        return server
    
    def sendText(self):
        phoneNumber = str(os.getenv("PHONE_NUM"))
        email = str(os.getenv("EMAIL"))
        sms_gateway = phoneNumber + "@vtext.com"
        server = self.getEmailServer()
        body = self._genericMessage()
        server.sendmail(email, sms_gateway, msg = body)
        # if first of month
        if datetime.now().day == 1:
            body = "\r\n\r\n" + self._firstOfTheMonthMessage()
            server.sendmail(email,  sms_gateway, msg = body)
        server.quit()
