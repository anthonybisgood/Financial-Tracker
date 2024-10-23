from BankInterface import BankInterface
import os
from dotenv import load_dotenv, dotenv_values
import smtplib

# from dotenv import load_dotenv
from datetime import datetime, timedelta


class ClientIO(object):

    def __init__(self, logger, bankInterface: BankInterface):
        load_dotenv()
        self.logger = logger
        self.bankInterface: BankInterface = bankInterface
        self.yesterdaysDate: datetime = datetime.date(datetime.now()) - timedelta(
            days=1
        )

    def getSpentThisWeek(self) -> float:
        today = datetime.date(datetime.now())
        start = today - timedelta(days=today.weekday()) - timedelta(days=1)
        end = start + timedelta(days=6)
        spent = -self.bankInterface.getSpentBetween(
            self.bankInterface._getAccountIDs("creditCard"), start, end
        )
        spent = round(spent, 2)
        self.logger.debug("Spent this week: %s", spent)
        return spent

    def percentOfWeeklyBudgetSpent(self) -> float:
        today = datetime.date(datetime.now())
        start = today - timedelta(days=today.weekday()) - timedelta(days=1)
        end = start + timedelta(days=6)
        dailyBudget = self.bankInterface.getProjectedBudget(start, end) / 14

        weeklyBudget = dailyBudget * 7
        spent = -self.bankInterface.getSpentBetween(
            self.bankInterface._getAccountIDs("creditCard"), start, end
        )
        percent_spent = round(spent / weeklyBudget * 100, 2)
        self.logger.debug("Percent of weekly budget spent: %s", percent_spent)
        return percent_spent

    def _getEarnedThisMonth(self) -> float:
        daysThisMonth = datetime.now().day
        firstOfThisMonth = datetime.date(datetime.now()) - timedelta(
            days=daysThisMonth - 1
        )
        lastOfThisMonth = datetime.date(datetime.now()) + timedelta(
            days=30 - daysThisMonth
        )
        earned = self.bankInterface.getProjectedBudget(
            firstOfThisMonth, lastOfThisMonth
        )
        self.logger.debug("Earned this month: %s", earned)
        return earned

    def percentOfMonthlyBudgetSpent(self) -> float:
        daysThisMonth = datetime.now().day
        firstOfThisMonth = datetime.date(datetime.now()) - timedelta(
            days=daysThisMonth - 1
        )
        budget = self._getEarnedThisMonth()
        credit_accounts = self.bankInterface._getAccountIDs("creditCard")
        today = datetime.date(datetime.now())
        spent = -self.bankInterface.getSpentBetween(
            credit_accounts, firstOfThisMonth, today
        )
        percent_spent = round(spent / budget * 100, 2)
        self.logger.debug("Percent of budget spent this month: %s", percent_spent)
        return percent_spent

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
        percent_spent = round(spent / budget * 100, 2)
        self.logger.debug("Percent of budget spent this year: %s", percent_spent)
        return percent_spent

    def _genericMessage(self) -> str:
        res = "\nSpent this Week: ${}".format(str(self.getSpentThisWeek()))
        res += "\nPercent of weekly budget spent:\n{}%".format(
            str(self.percentOfWeeklyBudgetSpent())
        )
        res += "\nPercent of monthly budget spent:\n{}%".format(
            str(self.percentOfMonthlyBudgetSpent())
        )
        res += "\r\n\r\n\r\n"
        return res

    def _firstOfTheMonthMessage(self) -> str:
        earned = self._getEarnedThisMonth()
        res = "Spent last month: ${}".format(earned)
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
        try:
            server = self.getEmailServer()
            self.logger.debug("Logged in to email server successfully")
        except Exception as e:
            self.logger.exception("Error logging in to email server: %s", e)
            return
        body = self._genericMessage()
        self.logger.info("Sending daily text message")
        server.sendmail(email, sms_gateway, msg=body)
        # if first of month
        if datetime.now().day == 1:
            self.logger.info("Sending monthly text message")
            body = "\r\n\r\n" + self._firstOfTheMonthMessage()
            server.sendmail(email, sms_gateway, msg=body)
        server.quit()
