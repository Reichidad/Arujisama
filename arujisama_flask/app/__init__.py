import os
from datetime import datetime, timedelta

import jwt
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from .common import common_func
from .common.response_code import Response_code
from .common.static_numbers import STATIC_NUMBERS
from .config import config_by_name
from flask_migrate import Migrate


config_name = os.getenv("cur_env") or "dev"

main_app = Flask(__name__)
main_app.config.from_object(config_by_name[config_name])

db = SQLAlchemy()

db.init_app(main_app)

from arujisama_flask.app.dbcode import tables

migrate = Migrate(main_app, db)


@main_app.route("/", methods=["GET", "POST"])
def rootPage():
    return redirect("/main")


@main_app.route("/main", methods=["GET", "POST"])
def mainPage():
    return render_template('main.html')


@main_app.errorhandler(404)
def page_not_found(error):
    return redirect("/main")


@main_app.route("/idexistcheck", methods=["GET", "POST"])
def idexistcheck():
    import arujisama_flask.app.dbcode.dbfunc as dbfunc

    # {URL}/idexistcheck?id=XXX&type=YYY의 형태로 보낸다

    id = ""
    if request.method == "GET":
        id = request.args.get("id", type=str)
        # type = request.args.get('type', type=str)
    elif request.method == "POST":
        id = request.get_json()["id"]
        # type = request.get_json()['type']

    # client단에서의 체크가 확실하면 지울부분
    # 길이는 2자 이상, 20자 이하. or 입력 없는지 체크
    id_length_limit = id is None or len(id) < STATIC_NUMBERS.ID_LENGTH_MIN or len(id) > STATIC_NUMBERS.ID_LENGTH_MAX

    if id_length_limit:
        return common_func.generate_response(401, code=Response_code.ID_LENGTH_LIMIT_FAIL)
    ########

    result = dbfunc.id_exist_check(id)
    return common_func.generate_response(200, code=result)


@main_app.route("/login", methods=["GET", "POST"])
def login():
    import arujisama_flask.app.dbcode.dbfunc as dbfunc

    ip = request.remote_addr

    # {URL}/login?id=XXX&pw=YYY의 형태로 보낸다.
    # PW는 평문상태로 온다.

    id, pw = "", ""
    if request.method == "GET":
        id = request.args.get("id", type=str)
        pw = request.args.get("pw", type=str)
    elif request.method == "POST":
        id = request.get_json()["id"]
        pw = request.get_json()["pw"]

    idlengthlimit = id is None or len(id) <= 1 or len(id) > 20
    if idlengthlimit:
        return common_func.generate_response(401, Response_code.ID_LENGTH_LIMIT_FAIL)

    result = dbfunc.login(id, pw, ip)
    if result == Response_code.LOGIN_SUCCESS:
        duration = datetime.now() + timedelta(seconds=60 * 60)
        payload = {
            "id": id,
            "exp": duration.strftime("%Y%m%d%H%M%S")
        }

        token = jwt.encode(payload, main_app.config["SECRET_KEY"], "HS256")
        # print(token)
        return common_func.generate_response(200, code=result, access_token=token.decode("UTF-8"))
    else:
        return common_func.generate_response(401, result)


@main_app.route("/signup", methods=["GET", "POST"])
def signup():
    import arujisama_flask.app.dbcode.dbfunc as dbfunc

    ip = request.remote_addr

    id, pw, name, email = "", "", "", ""
    if request.method == "GET":
        id = request.args.get("id", type=str)
        pw = request.args.get("pw", type=str)
        name = request.args.get("name", type=str)
        email = request.args.get("email", type=str)
    elif request.method == "POST":
        id = request.get_json()["id"]
        pw = request.get_json()["pw"]
        name = request.get_json()["name"]
        email = request.get_json()["email"]
    else:
        return common_func.generate_response(401, code=Response_code.SIGNUP_FAILED)

    result = dbfunc.signup(id, pw, name, email, ip)
    if result == Response_code.SIGNUP_SUCCESS:
        return common_func.generate_response(200, code=result)
    else:
        return common_func.generate_response(409, code=result)


@main_app.route("/tokencheck", methods=["GET", "POST"])
def tokencheck():
    import arujisama_flask.app.dbcode.dbfunc as dbfunc
    access_token = request.headers.get("Authorization")
    if access_token is not None:
        result, id = dbfunc.token_validation_check(access_token)
        print(result, id)
        if result == Response_code.TOKEN_INVALID:
            return common_func.generate_response(401, code=result)

        return common_func.generate_response(200, code=result)
    else:
        return common_func.generate_response(401, code=Response_code.TOKEN_INVALID)


@main_app.route("/removetestid", methods=["POST"])
def removetestid():
    import arujisama_flask.app.dbcode.dbfunc as dbfunc

    keycode = request.get_json()['keycode']
    if keycode == "superduperfantastickeycode":
        result = dbfunc.remove_test_id()
    else:
        result = Response_code.TEST_ID_REMOVE_ERROR

    if result == Response_code.TEST_ID_REMOVED:
        return common_func.generate_response(200, code=result)

    return common_func.generate_response(401, code=result)


@main_app.route("/loadstamp", methods=["GET", "POST"])
def loadstamp():
    import arujisama_flask.app.dbcode.dbfunc as dbfunc
    access_token = request.headers.get("Authorization")

    ip = request.remote_addr

    if access_token is not None:
        try:
            if request.method == "GET":
                page = request.args.get('page', type=int)
            elif request.method == "POST":
                page = request.get_json()['page']
            else:
                page = 0
        except TypeError as e:
            print(e)
            page = 0

        result, data = dbfunc.load_stamp(access_token, page, ip)

        if result == Response_code.LOAD_STAMP_FAILED:
            return common_func.generate_response(401, code=result, data=data)

        return common_func.generate_response(200, code=result, data=data)
    else:
        return common_func.generate_response(401, code=Response_code.TOKEN_INVALID)


@main_app.route("/addstamp", methods=["GET", "POST"])
def addstamp():
    import arujisama_flask.app.dbcode.dbfunc as dbfunc
    access_token = request.headers.get("Authorization")

    ip = request.remote_addr

    if access_token is not None:
        if request.method == "GET":
            memo = request.args.get('memo', type=str)
        elif request.method == "POST":
            memo = request.get_json()['memo']
        else:
            return common_func.generate_response(401, code=Response_code.ADD_STAMP_FAILED)

        result = dbfunc.add_stamp(access_token, memo, ip)

        if result == Response_code.ADD_STAMP_FAILED:
            return common_func.generate_response(401, code=result)

        return common_func.generate_response(200, code=result)

    else:
        return common_func.generate_response(401, code=Response_code.TOKEN_INVALID)


@main_app.route("/editstamp", methods=["GET", "POST"])
def editstamp():
    import arujisama_flask.app.dbcode.dbfunc as dbfunc
    access_token = request.headers.get("Authorization")

    ip = request.remote_addr

    if access_token is not None:
        if request.method == "GET":
            idx = request.args.get('stamp_idx', type=int)
            memo = request.args.get('edit_memo', type=str)
        elif request.method == "POST":
            idx = request.get_json()['stamp_idx']
            memo = request.get_json()['edit_memo']
        else:
            return common_func.generate_response(401, code=Response_code.ADD_STAMP_FAILED)

        result = dbfunc.edit_stamp(access_token, memo, idx, ip)

        return common_func.generate_response(200, code=result)
    else:
        return common_func.generate_response(401, code=Response_code.TOKEN_INVALID)


@main_app.route("/deletestamp", methods=["GET", "POST"])
def deletestamp():
    import arujisama_flask.app.dbcode.dbfunc as dbfunc
    access_token = request.headers.get("Authorization")

    ip = request.remote_addr

    if access_token is not None:
        if request.method == "GET":
            idx = request.args.get('stamp_idx', type=int)
        elif request.method == "POST":
            idx = request.get_json()['stamp_idx']
        else:
            return common_func.generate_response(401, code=Response_code.DELETE_STAMP_FAILED)

        result = dbfunc.delete_stamp(access_token, idx, ip)

        if result == Response_code.DELETE_STAMP_FAILED:
            return common_func.generate_response(401, code=result)

        return common_func.generate_response(200, code=result)

    else:
        return common_func.generate_response(401, code=Response_code.TOKEN_INVALID)


# @RE-A
# Validation : validation process를 위한 빈 페이지
# id-validation : RESTful API를 이용한 실제 인증 과정

@main_app.route("/validation/<token>", methods=["GET", "POST"])
def id_validation_test(token):
    return render_template('validation.html')


@main_app.route("/id-validation/<token>", methods=["GET", "POST"])
def id_validation(token):
    from arujisama_flask.app.email_func.id_validation import try_validation
    result = try_validation(token)
    return common_func.generate_response(200, code=result)


@main_app.route("/find-id", methods=["GET", "POST"])
def findid():
    import arujisama_flask.app.dbcode.dbfunc as dbfunc
    ip = request.remote_addr

    if request.method == "GET":
        name = request.args.get('name', type=str)
        email = request.args.get('email', type=str)
    elif request.method == "POST":
        name = request.get_json()['name']
        email = request.get_json()['email']
    else:
        return common_func.generate_response(401, code=Response_code.FIND_ID_FAILED)

    result, result_id = dbfunc.find_id(name, email, ip)

    if result == Response_code.FIND_ID_FAILED:
        return common_func.generate_response(401, code=result)

    return common_func.generate_response(200, code=result, data={"id": result_id})


@main_app.route("/find-pw", methods=["GET", "POST"])
def findpw():
    import arujisama_flask.app.dbcode.dbfunc as dbfunc
    ip = request.remote_addr

    if request.method == "GET":
        id = request.args.get('id', type=str)
        name = request.args.get('name', type=str)
        email = request.args.get('email', type=str)
    elif request.method == "POST":
        id = request.get_json()['id']
        name = request.get_json()['name']
        email = request.get_json()['email']
    else:
        return common_func.generate_response(401, code=Response_code.FIND_PW_FAILED)

    result = dbfunc.find_pw(id, name, email, ip)

    if result == Response_code.FIND_PW_FAILED:
        return common_func.generate_response(401, code=result)

    return common_func.generate_response(200, code=result)


@main_app.route("/reset-pw-page/<token>", methods=["GET", "POST"])
def resetpwpage(token):
    return render_template("reset-pw-page.html")


@main_app.route("/reset-pw/<token>", methods=["GET", "POST"])
def resetpw(token):
    import arujisama_flask.app.dbcode.dbfunc as dbfunc

    ip = request.remote_addr

    if request.method == "GET":
        pw = request.args.get('pw', type=str)
    elif request.method == "POST":
        pw = request.get_json()['pw']
    else:
        return common_func.generate_response(401, code=Response_code.RESET_PW_FAILED)

    result = dbfunc.reset_pw(token, pw, ip)

    return common_func.generate_response(200, code=result)
