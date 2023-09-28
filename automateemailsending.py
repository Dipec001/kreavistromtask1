import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import schedule
import time
import logging
import config


logging.basicConfig(filename="../task2/email_log.txt", level=logging.INFO)

MY_EMAIL = config.MY_EMAIL
MY_PASSWORD = config.MY_PASSWORD
HOME_DIRECTORY = os.path.expanduser("~")
REPORT_DIRECTORY = os.path.join(HOME_DIRECTORY, "testfolder")


def send_email(to_email):
    email_body = "Body of the email."

    message = MIMEMultipart()
    message["From"] = MY_EMAIL
    message["To"] = to_email
    message["Subject"] = "Title of the email"

    message.attach(MIMEText(email_body, "plain"))

    # Attach files from the report directory
    report_files = os.listdir(REPORT_DIRECTORY)
    for file_name in report_files:
        file_path = os.path.join(REPORT_DIRECTORY, file_name)
        try:
            attachment = MIMEApplication(open(file_path, "rb").read())
            attachment.add_header("Content-Disposition", "attachment", filename=file_name)
            message.attach(attachment)
        except Exception as e:
            print(f"Error attaching file {file_name}: {str(e)}")

    # Create a connection to the SMTP server
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            # Send the email
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=to_email, msg=message.as_string())
            logging.info(f"Email sent to {to_email}")
    except Exception as e:
        logging.error(f"Error sending email to {to_email}: {str(e)}")


# Read the recipient email addresses from a text file
with open("test.txt", "r") as file:
    recipient_emails = [line.strip() for line in file.readlines()]

# Schedule the script to run daily at 9:00 AM for each recipient
for email in recipient_emails:
    schedule.every().day.at("09:00").do(send_email, to_email=email)

while True:
    schedule.run_pending()
    time.sleep(60)
