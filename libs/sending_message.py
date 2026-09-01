import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from libs.settings import SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

global_list = []
global_message = []


def add_to_global_list(item):
    global_list.append(item)


def clear_global_list():
    global_list.clear()


def add_to_global_message(item):
    global_message.append(item)


def clear_global_message():
    global_message.clear()


def send_email_thread(server, username, password, from_mail, to_mail, content):
    """Поток отправки email"""
    try:
        server.login(username, password)
        server.sendmail(from_mail, to_mail, content)
        print(f"✅ Письмо успешно доставлено")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
    finally:
        server.quit()


def message_in_out(string, attach_file_list=None):
    """Отправка уведомления через email (SMTP_SSL)"""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = "Отчёт mass_loader"
        msg.attach(MIMEText(string, "plain", "utf-8"))

        if attach_file_list:
            for file_name in attach_file_list:
                if os.path.exists(file_name):
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(open(file_name, 'rb').read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_name))
                    msg.attach(part)
                else:
                    print(f"⚠️ Файл не найден: {file_name}")

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print(f"✅ Email отправлен на {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")
