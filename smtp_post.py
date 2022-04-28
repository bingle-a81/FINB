import os
import smtplib
from configparser import ConfigParser


def send_email(to_addr, subject, text, encode='utf-8'):
    """
    Отправка электронного письма (email)
    """

    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "email.ini")
    # проверка наличия файла `email.ini`
    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Конфигурация не найдена!")

    # извлечение переменных из конфигурации
    server = cfg.get("smtp", "server")
    port = cfg.get("smtp", "port")
    from_addr = cfg.get("smtp", "email")
    passwd = cfg.get("smtp", "passwd")
    charset = f'Content-Type: text/plain; charset={encode}'
    mime = 'MIME-Version: 1.0'
    # формируем тело письма
    body = "\r\n".join((f"From: {from_addr}", f"To: {to_addr}",
          f"Subject: {subject}", mime, charset, "", text))

    try:
        # подключаемся к почтовому сервису
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.ehlo()
        # логинимся на почтовом сервере
        smtp.login(from_addr, passwd)
        # пробуем послать письмо
        smtp.sendmail(from_addr, to_addr, body.encode(encode))
    except smtplib.SMTPException as err:
        print('Что - то пошло не так...')
        raise err
    finally:
        smtp.quit()

if __name__ == "__main__":
    with open('C:\\Users\\Programmer\\Desktop\\BDUP\\debug.log') as r:
        a=r.read()
    to_addr = "workmy327@aol.com"
    subject = "Test from Python."
    text = a
    send_email(to_addr, subject, text)