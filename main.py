import smtplib
import time
import logging
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Timer

#Setup logging
logging.basicConfig(filename='email_scheduler.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

#Email configuration
EMAIL_ADDRESS='youremail@gmail.com'
EMAIL_PASSWORD='your_app_password'
SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=587

#Function to send email
def send_email(to_address, subject, body):
    try:
        msg=MIMEMultipart()
        msg['From']=EMAIL_ADDRESS
        msg['To']=to_address
        msg['Subject']=subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_address, msg.as_string())

        logging.info(f"Email sent to {to_address} with subject '{subject}'")
    except Exception as e:
        logging.error(f"Failed to send email to {to_address}: {str(e)}")

#Function to schedule an email
def schedule_email(to_address, subject, body, send_time):
    delay=(send_time - datetime.now()).total_seconds()
    if delay<0:
        logging.warning(f"Send time for email to {to_address} is in the past.")
        return
    Timer(delay, send_email, args=[to_address, subject, body]).start()
    logging.info(f"Email to {to_address} scheduled for {send_time}")

#Function for recurring emails
def schedule_recurring_email(to_address, subject, body, start_time, interval_minutes):
    def send_and_reschedule():
        send_email(to_address, subject, body)
        next_send_time=datetime.now() + timedelta(minutes=interval_minutes)
        schedule_recurring_email(to_address, subject, body, next_send_time, interval_minutes)

    delay=(start_time - datetime.now()).total_seconds()
    if delay<0:
        logging.warning(f"Start time for recurring email to {to_address} is in the past.")
        return
    Timer(delay, send_and_reschedule).start()
    logging.info(f"Recurring email to {to_address} scheduled to start at {start_time} with interval of {interval_minutes} minutes")

#Example usage
if __name__ == "__main__":
    #Schedule a one-time email (Testing)
    schedule_email(
        to_address='recipient@gmail.com',
        subject='Birthday Reminder',
        body='Happy Birthday! Have a great day!',
        send_time=datetime(2023, 12, 24, 10, 0, 0)  #Send on Dec 24, 2023 at 10:00 AM
    )

    #Schedule a recurring email
    schedule_recurring_email(
        to_address='recipient@gmail.com',
        subject='Weekly Update',
        body='This is your weekly update!',
        start_time=datetime(2023, 12, 24, 10, 0, 0),  #Start on Dec 24, 2023 at 10:00 AM
        interval_minutes=10080  #Repeat every week (10080 minutes)
    )
