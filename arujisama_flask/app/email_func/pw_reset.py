import datetime
import jwt

from arujisama_flask.app import main_app
from .sending import *


def send_pw_reset_email(id, name, email):
    duration = datetime.datetime.now() + datetime.timedelta(seconds=60 * 5)
    payload = {
        "id": id,
        "exp": duration.strftime('%Y%m%d%H%M%S')
    }

    token = jwt.encode(payload, main_app.config["SECRET_KEY"], "HS256")

    content = """
{0}님의 비밀번호 초기화 이메일입니다.

초기화 링크: http://{1}/reset-pw-page/{2}

링크의 유효기간은 발송으로부터 5분입니다.    
""".format(name, "localhost:3781", token.decode("UTF-8"))

    title = "스탬프 웹사이트 비밀번호 찾기 이메일입니다."

    send_email_result = send_email(email=email, title=title, content=content)

    if send_email_result:
        return Response_code.RESET_PW_MAIL_SUCCESS
    else:
        return Response_code.RESET_PW_MAIL_FAILED
