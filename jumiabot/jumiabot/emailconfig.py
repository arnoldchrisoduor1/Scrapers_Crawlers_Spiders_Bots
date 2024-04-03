import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import json
import datetime
import pandas as pd

# Sender and recipient email addresses
sender_email = "digitalwilderness9@gmail.com"
recipient_email = "arnoldchris262@gmail.com"

# App-specific password generated from Google Account settings
app_specific_password = ""

# Get the current date in the desired format
current_date = datetime.datetime.now().strftime('%d %B, %Y')

# Email content
subject = f"JUMIA CRAWLER DATA  - {current_date}"
body = "The following is data "

# Create a MIMEMultipart object to represent the email
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# Read the JSON lines and create a DataFrame
with open("output.jsonl", "r", encoding="utf-8") as file:
    json_lines = file.readlines()

# Convert JSON lines to a DataFrame
data = [json.loads(line) for line in json_lines]
df = pd.DataFrame(data)

# Generate file names with the current date
date_str = datetime.datetime.now().strftime('%d%m%y')
csv_file_name = f"data_{date_str}.csv"
excel_file_name = f"data_{date_str}.xlsx"

# Write the DataFrame to CSV and Excel files
df.to_csv(csv_file_name, index=False)
df.to_excel(excel_file_name, index=False)

# Attach CSV file
with open(csv_file_name, "rb") as file:
    part = MIMEApplication(file.read(), Name=csv_file_name)
part['Content-Disposition'] = f'attachment; filename="{csv_file_name}"'
message.attach(part)

# Attach Excel file
with open(excel_file_name, "rb") as file:
    part = MIMEApplication(file.read(), Name=excel_file_name)
part['Content-Disposition'] = f'attachment; filename="{excel_file_name}"'
message.attach(part)

# Attach text version of scrapy.log
with open("scrapy.log", "r") as file:
    text_attachment = MIMEText(file.read())
text_attachment.add_header("Content-Disposition", "attachment", filename="scrapy.log")
message.attach(text_attachment)

try:
    # Connect to Gmail's SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # Log in using the app-specific password
    server.login(sender_email, app_specific_password)

    # Send the email
    server.sendmail(sender_email, recipient_email, message.as_string())
    print("Email sent successfully")

except smtplib.SMTPAuthenticationError as e:
    print(f"Failed to send email: {e}")

finally:
    # Close the connection to the SMTP server
    server.quit()
