from BankInterface import BankInterface
import os
from dotenv import load_dotenv, dotenv_values
import smtplib
# from dotenv import load_dotenv
from datetime import datetime, timedelta


class ClientIO(object):

    def __init__(self, bankInterface: BankInterface):
        load_dotenv()
        self.bankInterface: BankInterface = bankInterface
        self.yesterdaysDate: datetime = datetime.date(datetime.now()) - timedelta(
            days=1
        )

    def percentOfWeeklyBudgetSpent(self) -> float:
        today = datetime.date(datetime.now())
        start = today - timedelta(days=today.weekday()) - timedelta(days=1)
        end = start + timedelta(days=6)
        dailyBudget = self.bankInterface.getProjectedBudget(start, end)
        weeklyBudget = dailyBudget * 7
        spent = -self.bankInterface.getSpentBetween(
            self.bankInterface._getAccountIDs("creditCard"), start, end
        )
        return round(spent / weeklyBudget * 100, 2)

    def percentOfMonthlyBudgetSpent(self) -> float:
        daysThisMonth = datetime.now().day
        firstOfThisMonth = datetime.date(datetime.now()) - timedelta(
            days=daysThisMonth - 1
        )
        lastOfThisMonth = datetime.date(datetime.now()) + timedelta(
            days=30 - daysThisMonth
        )
        budget = self.bankInterface.getProjectedBudget(
            firstOfThisMonth, lastOfThisMonth
        )
        credit_accounts = self.bankInterface._getAccountIDs("creditCard")
        today = datetime.date(datetime.now())
        spent = -self.bankInterface.getSpentBetween(
            credit_accounts, firstOfThisMonth, today
        )
        return round(spent / budget * 100, 2)

    def percentOfYearlyBudgetSpent(self) -> float:
        beginning_of_year = datetime.date(datetime.now()) - timedelta(
            days=datetime.now().timetuple().tm_yday - 1
        )
        end_of_year = datetime.date(datetime.now()) + timedelta(
            days=365 - datetime.now().timetuple().tm_yday
        )
        budget = self.bankInterface.getProjectedBudget(beginning_of_year, end_of_year)
        spent = -self.bankInterface.getSpentBetween(
            self.bankInterface._getAccountIDs("creditCard"),
            beginning_of_year,
            datetime.date(datetime.now()),
        )
        return round(spent / budget * 100, 2)

    def getBudget(self, pastTime: int) -> float:
        earned: float = self.bankInterface.getEarnedBetween(
            self.bankInterface._getAccountIDs("checking"),
            datetime.date(datetime.now()) - timedelta(days=pastTime),
            datetime.date(datetime.now()) + timedelta(days=2),
        )
        spent: float = self.bankInterface.getSpentBetween(
            self.bankInterface._getAccountIDs("creditCard"),
            datetime.date(datetime.now()) - timedelta(days=pastTime),
            datetime.date(datetime.now()) + timedelta(days=2),
        )
        utils: float = self.bankInterface.getSpentBetween(
            self.bankInterface._getAccountIDs("checking"),
            datetime.date(datetime.now()) - timedelta(days=pastTime),
            datetime.date(datetime.now()) + timedelta(days=2),
        )
        return round(spent / (earned - utils) * 100, 2)

    def _genericMessage(self) -> str:
        res = "\nSpent yesterday: ${}".format(
            str(self.bankInterface.getSpentYesterday())
        )
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
        email = str(os.getenv("EMAIL"))
        pas = str(os.getenv("APP_PASS"))
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
        server.sendmail(email, sms_gateway, msg=body)
        # if first of month
        if datetime.now().day == 1:
            body = "\r\n\r\n" + self._firstOfTheMonthMessage()
            server.sendmail(email, sms_gateway, msg=body)
        server.quit()
