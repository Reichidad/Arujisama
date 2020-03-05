import smtplib
import json

from arujisama_flask.app.common.common_func import get_cwd_directory
from ..common.response_code import Response_code
from email.mime.text import MIMEText
from ..common.log_writer import write_log

if __name__ == '__main__':
    directory = get_cwd_directory('/../config_files/')
else:
    directory = get_cwd_directory('/app/config_files/')


def send_email(email, title="제목을 입력해주세요", content="내용을 입력해주세요"):
    mail_info_file = directory + 'mailinfo.json'

    try:
        with open(mail_info_file, mode="r") as fp:
            mail_infos = json.load(fp)

    except FileNotFoundError as e:
        write_log(Response_code.SEND_VALIDATE_EMAIL_FAILED, id=id, func="send_validation_email")
        return False

    session = smtplib.SMTP('smtp.gmail.com', 587)

    session.starttls()

    session.login(mail_infos['id'], mail_infos['pw'])

    msg = MIMEText(content)
    msg['Subject'] = title

    session.sendmail(mail_infos['id'] + "@gmail.com", email, msg.as_string())

    session.quit()

    return True
