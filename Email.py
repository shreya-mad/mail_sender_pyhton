import smtplib
import re
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv


load_dotenv()
# ---------- CONFIG ----------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# SENDER_EMAIL = "smadeshiya12345@gmail.com"
# SENDER_PASSWORD = "govs pagx blsj alei" 


RESUME_FILE = "Shreya_Madeshiya_Resume.pdf"

SUBJECT = "Application for Software Developer"

BODY = """
Hello,

I hope you’re doing well.

I’m writing to apply for the Software Developer role. I have 2.4 years of
hands-on experience in building web applications, with a strong focus on
clean UI, performance, and maintainable code.

I have worked extensively with HTML, CSS, React.js, JavaScript, TypeScript,
Node.js, Express.js, MongoDB, SQL, and REST API integration. I’m comfortable
collaborating using Git and modern development workflows.

I’ve attached my resume for your review and would be happy to discuss how
my experience can contribute to your team.

Thank you for your time and consideration.

Warm regards,
Shreya Madeshiya
"""

# ---------- EMAIL VALIDATION ----------
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

# ---------- READ HR EMAILS ----------
with open("hrs.txt", "r") as file:
    hr_emails = [line.strip() for line in file if line.strip()]

total_emails = len(hr_emails)
sent_count = 0
error_count = 0
invalid_count = 0

# ---------- SMTP LOGIN ----------
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(SENDER_EMAIL, SENDER_PASSWORD)

# ---------- SEND EMAILS ----------
for hr in hr_emails:

    # Skip invalid email format
    if not is_valid_email(hr):
        print(f"❌ Invalid email skipped: {hr}")
        invalid_count += 1
        continue

    try:
        msg = MIMEMultipart()
        msg["From"] = "Shreya Madeshiya | Software Developer <smadeshiya12345@gmail.com>"
        msg["To"] = hr
        msg["Subject"] = SUBJECT

        msg.attach(MIMEText(BODY, "plain"))

        # Attach resume
        with open(RESUME_FILE, "rb") as resume:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(resume.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{RESUME_FILE}"'
        )
        msg.attach(part)

        server.sendmail(SENDER_EMAIL, hr, msg.as_string())
        print(f"✅ Mail sent to {hr}")
        sent_count += 1

        time.sleep(3)  # avoid spam

    except smtplib.SMTPException as e:
        print(f"❌ Error sending to {hr}: {e}")
        error_count += 1

server.quit()

# ---------- FINAL SUMMARY ----------
print("\n========== EMAIL SUMMARY ==========")
print(f"📩 Total emails in file   : {total_emails}")
print(f"✅ Successfully sent     : {sent_count}")
print(f"❌ Failed due to errors  : {error_count}")
print(f"⚠️ Invalid emails skipped: {invalid_count}")
print("===================================")

