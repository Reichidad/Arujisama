from arujisama_flask.app import main_app
from arujisama_flask.app import db
from arujisama_flask.app.dbcode import tables
from sqlalchemy import and_, desc
from arujisama_flask.app.common.static_numbers import STATIC_NUMBERS
from arujisama_flask.app.common.response_code import Response_code
from arujisama_flask.app.common.resp_string import response_string
from arujisama_flask.app.common.log_writer import write_log
from arujisama_flask.app.email_func import pw_reset
from sqlalchemy.exc import SQLAlchemyError
import hashlib
import datetime
import jwt


def add_query(row):  # insert query
    try:
        db.session.add(row)
        db.session.commit()
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()


def delete_query(row):  # delete query
    try:
        row.delete()
        db.session.commit()
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()


def check_stamp_redundancy(stamp_time):
    current_time = datetime.datetime.now()
    if stamp_time.hour < 5:
        stamp_time = stamp_time + datetime.timedelta(days=-1)
    if current_time.hour < 5:
        current_time = current_time + datetime.timedelta(days=-1)

    # 시간 단위로는 버려내서 요일 단위로 비교
    stamp_time = stamp_time.strftime("%Y%m%d")
    current_time = current_time.strftime("%Y%m%d")

    if stamp_time < current_time:  # stamp_time < current_time이라는건 날짜가 바뀐 것
        return True
    else:
        return False


def id_exist_check(id, validoption='O'):
    try:
        result = tables.UserAccount.query.filter(
            and_(
                tables.UserAccount.id == id
            )
        ).all()
    except SQLAlchemyError as e:
        print(e)
        return Response_code.DB_ERROR

    return {
        0: Response_code.ID_NOT_EXIST,
        1: Response_code.ID_EXIST,
        2: Response_code.ID_MORE_THAN_ONE
    }.get(len(result), Response_code.ID_MORE_THAN_ONE)


def login(id, pw, ip="0.0.0.0"):
    hashed_pw = hashlib.sha256(pw.encode()).hexdigest()
    try:
        result = tables.UserAccount.query.filter(
            and_(
                tables.UserAccount.id == id,
                tables.UserAccount.pw == hashed_pw
            )
        ).all()
    except SQLAlchemyError as e:
        print(e)
        write_log(log=response_string(Response_code.DB_ERROR), ip=ip, id=id, func="login")
        return Response_code.DB_ERROR

    result_count = len(result)

    if result_count == 0:
        result_code = Response_code.LOGIN_FAILED
    elif result_count == 1:
        result_code = Response_code.LOGIN_SUCCESS
    else:
        result_code = Response_code.DBFUNC_UNEXPECTED

    write_log(log=response_string(result_code), ip=ip, id=id, func="login")
    return result_code


def signup(id, pw, name, email, ip="0.0.0.0"):
    # from ..email_func.id_validation import send_validation_email
    if id_exist_check(id) == Response_code.ID_EXIST:
        write_log(log=response_string(Response_code.ID_EXIST), ip=ip, id=id, func="signup")
        return Response_code.SIGNUP_FAILED
    else:
        hashed_pw = hashlib.sha256(pw.encode()).hexdigest()
        try:
            '''
            email_result = send_validation_email(id, name, email)
            if email_result == Response_code.SEND_VALIDATE_EMAIL_FAILED:
                return Response_code.SIGNUP_FAILED
            else:
            '''
            add_query(tables.UserAccount(id=id, pw=hashed_pw, submitdate=datetime.datetime.now()))
            add_query(tables.UserInfo(id=id, name=name, email=""))
            write_log(log=response_string(Response_code.SIGNUP_SUCCESS), ip=ip, id=id, func="signup")
            return Response_code.SIGNUP_SUCCESS
        except SQLAlchemyError as e:
            print(e)
            write_log(log=response_string(Response_code.DB_ERROR), ip=ip, id=id, func="signup")
            return Response_code.DB_ERROR


def validate_id(id):
    try:
        row = tables.UserAccount.query.filter_by(id=id).first()

        print(row.current_valid)

        if row.current_valid == 'O':
            result_code = Response_code.ALREADY_VALIDATED_ID
        else:
            row.query.update(dict(current_valid='O'))
            row2 = tables.UserInfo.query.filter_by(id=id).update(dict(current_valid='O'))
            db.session.commit()

            result_code = Response_code.VALIDATE_ID_SUCCESS

    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        result_code = Response_code.VALIDATE_ID_FAILED

    write_log(log=response_string(result_code), id=id, func='validate_id')
    return result_code


def remove_test_id():
    try:
        row = tables.UserAccount.query.filter_by(id='testid')
        delete_query(row)
        write_log(log=response_string(Response_code.TEST_ID_REMOVED), id='testid', func="remove_testid")
        return Response_code.TEST_ID_REMOVED
    except SQLAlchemyError as e:
        print(e)
        write_log(log=response_string(Response_code.TEST_ID_REMOVE_ERROR), id='testid', func="remove_testid")
        return Response_code.TEST_ID_REMOVE_ERROR


def token_validation_check(token):
    try:
        payload = jwt.decode(token, main_app.config["SECRET_KEY"], "HS256")
    except jwt.InvalidTokenError:
        return Response_code.TOKEN_INVALID, ""

    id = payload['id']
    exp = payload['exp']

    valid_id = id_exist_check(id)
    if valid_id == Response_code.ID_NOT_EXIST:
        return Response_code.TOKEN_INVALID, ""

    valid_exp = datetime.datetime.now().strftime('%Y%m%d%H%M%S') < exp
    if not valid_exp:
        return Response_code.TOKEN_INVALID, ""

    return Response_code.TOKEN_VALID, id


def load_stamp(token, page=0, ip="0.0.0.0"):
    valid_token, id = token_validation_check(token)
    if valid_token == Response_code.TOKEN_VALID:
        # id = jwt.decode(token, main_app.config["SECRET_KEY"], "HS256")['id']

        rows = tables.StampBox.query.filter(
            and_(
                tables.StampBox.id == id,
                tables.StampBox.validstamp == 'O'
            )
        ).all()
        count = len(rows)

        if page == 0:
            start = count // STATIC_NUMBERS.STAMP_MAX_IN_ONE_CARD * STATIC_NUMBERS.STAMP_MAX_IN_ONE_CARD
            end = count
        else:
            start = 0 + (page - 1) * STATIC_NUMBERS.STAMP_MAX_IN_ONE_CARD
            end = count \
                if page * STATIC_NUMBERS.STAMP_MAX_IN_ONE_CARD > count \
                else page * STATIC_NUMBERS.STAMP_MAX_IN_ONE_CARD

        list = []
        for i in range(start, end):
            try:
                list.append(dict(
                    submitdate=rows[i].submitdate,
                    memo=rows[i].memo,
                    idx=rows[i].idx
                ))
            except IndexError as ie:
                write_log(log=str(ie), ip=ip, id=id, func="load_stamp")
                print(ie)

        try:
            most_recent_stamp = tables.StampBox.query.filter(
                and_(
                    tables.StampBox.id == id,
                    tables.StampBox.validstamp == 'O'
                )
            ).order_by(desc(tables.StampBox.submitdate)).first()
            last_stamp_date = most_recent_stamp.submitdate
        except AttributeError as e:
            print("load_stamp most_recent_stamp load error")
            write_log(log=str(e), ip=ip, id=id, func="load_stamp")
            print(e)
            last_stamp_date = ''

        result_data = {"count": count, "stamp_list": list, "last_stamp_date": last_stamp_date}
        write_log(log=response_string(Response_code.LOAD_STAMP_SUCCESS), ip=ip, id=id, func="load_stamp")
        return Response_code.LOAD_STAMP_SUCCESS, result_data

    else:
        write_log(log=response_string(Response_code.LOAD_STAMP_FAILED), ip=ip, func="load_stamp")
        return Response_code.LOAD_STAMP_FAILED, None


def add_stamp(token, memo, ip="0.0.0.0"):
    valid_token, id = token_validation_check(token)

    if valid_token == Response_code.TOKEN_VALID:
        # id = jwt.decode(token, main_app.config["SECRET_KEY"], "HS256")['id']
        try:
            most_recent_stamp = tables.StampBox.query.filter(
                and_(
                    tables.StampBox.id == id,
                    tables.StampBox.validstamp == 'O'
                )
            ).order_by(desc(tables.StampBox.submitdate)).first()

            stamp_time = most_recent_stamp.submitdate

            daily_redendancy_check = check_stamp_redundancy(stamp_time)
        except AttributeError as e:
            daily_redendancy_check = True  # 여기에 오는건 스탬프 자체가 안 찍혀있는 것

        if daily_redendancy_check:
            add_query(tables.StampBox(id=id, submitdate=datetime.datetime.now(), memo=memo, validstamp='O'))

            write_log(log=response_string(Response_code.ADD_STAMP_SUCCESS), ip=ip, id=id, func="add_stamp")
            return Response_code.ADD_STAMP_SUCCESS
        else:
            write_log(log=response_string(Response_code.ADD_STAMP_ALREADY), ip=ip, id=id, func="add_stamp")
            return Response_code.ADD_STAMP_ALREADY
    else:
        write_log(log=response_string(Response_code.ADD_STAMP_FAILED), ip=ip, func="add_stamp")
        return Response_code.ADD_STAMP_FAILED


def edit_stamp(token, memo, idx, ip="0.0.0.0"):
    valid_token, id = token_validation_check(token)
    if valid_token == Response_code.TOKEN_VALID:
        # id = jwt.decode(token, main_app.config["SECRET_KEY"], "HS256")['id']
        try:
            most_recent_stamp = tables.StampBox.query.filter(
                and_(
                    tables.StampBox.id == id,
                    tables.StampBox.validstamp == "O"
                )
            ).order_by(desc(tables.StampBox.submitdate)).first()

            stamp_idx = most_recent_stamp.idx
            if stamp_idx != idx:
                write_log(log=response_string(Response_code.EDIT_STAMP_NOT_MOST_RECENT), ip=ip, func="edit_stamp",
                          memo="not most recent stamp")
                return Response_code.EDIT_STAMP_NOT_MOST_RECENT

            most_recent_stamp.memo = memo
            db.session.commit()

            write_log(log=response_string(Response_code.EDIT_STAMP_SUCCESS), ip=ip, func="edit_stamp", memo="success")
            return Response_code.EDIT_STAMP_SUCCESS

        except SQLAlchemyError as e:
            db.session.rollback()
            write_log(log=response_string(Response_code.EDIT_STAMP_FAILED), ip=ip, func="edit_stamp",
                      memo="sqlalchemy error")
            return Response_code.EDIT_STAMP_FAILED
    else:
        write_log(log=response_string(Response_code.EDIT_STAMP_FAILED), ip=ip, func="edit_stamp", memo="token_invalid")
        return Response_code.EDIT_STAMP_FAILED


def delete_stamp(token, idx, ip="0.0.0.0"):
    valid_token, id = token_validation_check(token)

    if valid_token == Response_code.TOKEN_VALID:
    # id = jwt.decode(token, main_app.config["SECRET_KEY"], "HS256")['id']
        try:
            most_recent_stamp = tables.StampBox.query.filter(
                and_(
                    tables.StampBox.id == id,
                    tables.StampBox.validstamp == 'O'
                )
            ).order_by(desc(tables.StampBox.submitdate)).first()

            stamp_idx = most_recent_stamp.idx

            if stamp_idx != idx:
                write_log(log=response_string(Response_code.EDIT_STAMP_NOT_MOST_RECENT), ip=ip, func="edit_stamp",
                          memo="not most recent stamp")
                return Response_code.EDIT_STAMP_NOT_MOST_RECENT

            db.session.delete(most_recent_stamp)
            db.session.commit()

            write_log(log=response_string(Response_code.DELETE_STAMP_SUCCESS), ip=ip, id=id, func="delete_stamp")
            return Response_code.DELETE_STAMP_SUCCESS

        except SQLAlchemyError as e:
            db.session.rollback()
            write_log(log=response_string(Response_code.DELETE_STAMP_FAILED), ip=ip, func="edit_stamp",
                      memo="sqlalchemy error")
            return Response_code.DELETE_STAMP_FAILED
        '''
        try:
            for idx in idxs:
                stmt = tables.StampBox.query.filter_by(idx=idx).update(dict(validstamp="X"))
                db.session.commit()
            write_log(log=response_string(Response_code.DELETE_STAMP_SUCCESS), ip=ip, id=id, func="delete_stamp")
            return Response_code.DELETE_STAMP_SUCCESS
        except SQLAlchemyError as e:
            print(e)
            write_log(log=response_string(Response_code.DB_ERROR), ip=ip, id=id, func="delete_stamp")
            return Response_code.DB_ERROR
        '''
    else:
        write_log(log=response_string(Response_code.DELETE_STAMP_FAILED), ip=ip, func="delete_stamp")
        return Response_code.DELETE_STAMP_FAILED



def find_id(name, email, ip="0.0.0.0"):
    # id 찾기
    try:
        result = tables.UserInfo.query.filter(
            and_(
                tables.UserInfo.name == name,
                tables.UserInfo.email == email,
                tables.UserInfo.current_valid == "O"
            )
        ).all()

        if len(result) > 1:
            write_log(log=response_string(Response_code.DBFUNC_UNEXPECTED), ip=ip, func="find_id",
                      memo="name: {0}, email: {1}".format(name, email))
            return Response_code.DBFUNC_UNEXPECTED, None
        elif len(result) == 0:
            write_log(log=response_string(Response_code.FIND_ID_FAILED), ip=ip, func="find_id",
                      memo="name: {0}, email: {1}".format(name, email))
            return Response_code.FIND_ID_FAILED, None
        else:
            result_id = result[0].id
            id_length = len(result_id)

            result_id = result_id[0:int(id_length / 2)] + "*" * (id_length - int(id_length / 2))

            write_log(log=response_string(Response_code.FIND_ID_SUCCESS), ip=ip, func="find_pw",
                      memo="name: {0}, email: {1}".format(name, email))
            return Response_code.FIND_ID_SUCCESS, result_id

    except SQLAlchemyError as e:
        print(e)
        write_log(log=response_string(Response_code.DB_ERROR), ip=ip, func="find_id",
                  memo="name: {0}, email: {1}".format(name, email))
        return Response_code.DB_ERROR


def find_pw(id, name, email, ip="0.0.0.0"):
    # pw 찾기 (올바르면 비밀번호 초기화 이메일 전송함)
    try:
        result = tables.UserInfo.query.filter(
            and_(
                tables.UserInfo.id == id,
                tables.UserInfo.name == name,
                tables.UserInfo.email == email,
                tables.UserInfo.current_valid == "O"
            )
        ).all()

        if len(result) > 1:
            write_log(log=response_string(Response_code.DBFUNC_UNEXPECTED), ip=ip, func="find_pw",
                      memo="name: {0}, email: {1}".format(name, email))
            return Response_code.DBFUNC_UNEXPECTED
        elif len(result) == 0:
            write_log(log=response_string(Response_code.FIND_PW_FAILED), ip=ip, func="find_pw",
                      memo="name: {0}, email: {1}".format(name, email))
            return Response_code.FIND_PW_FAILED
        else:
            pw_reset.send_pw_reset_email(id=id, name=name, email=email)

            write_log(log=response_string(Response_code.FIND_PW_SUCCESS), ip=ip, func="find_pw",
                      memo="name: {0}, email: {1}".format(name, email))
            return Response_code.FIND_PW_SUCCESS


    except SQLAlchemyError as e:
        print(e)
        write_log(log=response_string(Response_code.DB_ERROR), ip=ip, func="find_pw",
                  memo="name: {0}, email: {1}".format(name, email))
        return Response_code.DB_ERROR


def reset_pw(token, pw, ip="0.0.0.0"):
    # 비밀번호 초기화
    valid_token, id = token_validation_check(token)

    if valid_token == Response_code.TOKEN_VALID:
        try:
            hashed_pw = hashlib.sha256(pw.encode()).hexdigest()

            stmt = tables.UserAccount.query.filter(
                and_(
                    tables.UserAccount.id == id,
                    tables.UserAccount.current_valid == "O"
                )
            ).update(dict(pw=hashed_pw))
            db.session.commit()

            write_log(log=response_string(Response_code.RESET_PW_SUCCESS), ip=ip, func="reset_pw",
                      memo="{0} 비밀번호 리셋됨".format(id))
            return Response_code.RESET_PW_SUCCESS
        except SQLAlchemyError as e:
            db.session.rollback()

            write_log(log=response_string(Response_code.RESET_PW_FAILED), ip=ip, func="reset_pw")
            return Response_code.RESET_PW_FAILED

    else:
        write_log(log=response_string(Response_code.TOKEN_INVALID), ip=ip, func="reset_pw")
