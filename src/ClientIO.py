from BankInterface import BankInterface
from CSVInterface import CSVInterface
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


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

    def _genericMessage(self) -> str:
        res = "Spent yesterday: ${}".format(str(self.bankInterface.getDailySpent()))
        res += "\nPercent of weekly budget spent: {}%".format(
            str(self.percentOfWeeklyBudgetSpent())
        )
        res += "\nPercent of monthly budget spent: {}%".format(
            str(self.percentOfMonthlyBudgetSpent())
        )
        res += "\n"
        return res
    
    def _firstOfTheMonthMessage(self) -> str:
        res = "Spent this month: ${}".format(str(self.csvInterface.getMonthlyEarned()))
        res += "\nPercent of yearly budget spent: {}%".format(
            str(self.percentOfYearlyBudgetSpent())
        )
        res += "\n"
        return res

    def sendText(self, body):
        load_dotenv()
        email = str(os.getenv("EMAIL"))
        pas = str(os.getenv("EMAIL_PASS"))
        phoneNumber = str(os.getenv("PHONE_NUM"))
        sms_gateway = phoneNumber + "@vtext.com"
        # The server we use to send emails in our case it will be gmail but every email provider has a different smtp
        # and port is also provided by the email provider.
        smtp = "smtp.gmail.com"
        port = 587

        # Now we use the MIME module to structure our message.
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = sms_gateway
        # Make sure you add a new line in the subject
        msg["Subject"] = "\n"
        body = "\r\n\r\n"+body
        # Make sure you also add new lines to your body
        # and then attach that body furthermore you can also send html content.
        msg.attach(MIMEText(body.encode("utf-8"), "plain", "utf-8"))

        # This will start our email server
        server = smtplib.SMTP(smtp, port)
        # Starting the server
        server.starttls()
        # Now we need to login
        server.login(msg["From"], pas)
        server.sendmail(msg["From"] , msg["To"],body)
        server.quit()

