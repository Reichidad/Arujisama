import datetime
import jwt

from arujisama_flask.app import main_app
from ..dbcode import dbfunc
from .sending import *
from arujisama_flask.app.common.common_func import get_cwd_directory

if __name__ == '__main__':
    directory = get_cwd_directory('/../config_files/')
else:
    directory = get_cwd_directory('/app/config_files/')


def send_validation_email(id, name, email):  # signup할때 오므로 id_exist_check는 skip
    duration = datetime.datetime.now() + datetime.timedelta(seconds=60 * 60)
    payload = {
        "id": id,
        "exp": duration.strftime('%Y%m%d%H%M%S')
    }

    token = jwt.encode(payload, main_app.config["SECRET_KEY"], "HS256")

    content = """
{0}님의 스탬프 웹사이트 인증 이메일입니다.

인증 링크: http://{1}/validation/{2}

링크의 유효기간은 발송으로부터 1시간입니다.
""".format(name, "localhost:3781", token.decode("UTF-8"))

    title = '스탬프 웹사이트 인증 이메일입니다.'

    send_email_result = send_email(email=email, title=title, content=content)

    if send_email_result:
        return Response_code.SEND_VALIDATE_EMAIL_SUCCESS
    else:
        return Response_code.SEND_VALIDATE_EMAIL_FAILED


def try_validation(token):
    try:
        payload = jwt.decode(token, main_app.config["SECRET_KEY"], "HS256")

    except jwt.InvalidTokenError as e:
        return Response_code.TOKEN_INVALID

    id = payload['id']
    exp = payload['exp']

    valid_exp = datetime.datetime.now().strftime('%Y%m%d%H%M%S') < exp

    if not valid_exp:
        return Response_code.VALIDATE_ID_FAILED

    return dbfunc.validate_id(id)
