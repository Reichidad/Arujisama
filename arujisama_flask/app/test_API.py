import pytest
import json
import hashlib
from .common.response_code import Response_code
from app import main_app


@pytest.fixture
def client():
    client = main_app.test_client()

    yield client


def test_idexistcheck_exist(client):
    result = client.post(
        "/idexistcheck",
        data=json.dumps({"id": "test"}),
        content_type="application/json"
    )
    result_json = json.loads(result.data.decode("utf-8"))
    assert result.status_code == 200
    assert result_json["code"] == Response_code.ID_EXIST


def test_idexistcheck_not_exist(client):
    result = client.post(
        "/idexistcheck",
        data=json.dumps({"id": "superduperid"}),
        content_type="application/json"
    )
    result_json = json.loads(result.data.decode("utf-8"))
    assert result.status_code == 200
    assert result_json["code"] == Response_code.ID_NOT_EXIST


def test_login_success(client):
    result = client.post(
        "/login",
        data=json.dumps({"id": "test", "pw": "test"}),
        content_type="application/json"
    )
    result_json = json.loads(result.data.decode("utf-8"))
    assert result.status_code == 200
    assert result_json["code"] == Response_code.LOGIN_SUCCESS


def test_login_failed(client):
    result = client.post(
        "/login",
        data=json.dumps({"id": "superduperid", "pw": "superduperpw"}),
        content_type="application/json"
    )
    result_json = json.loads(result.data.decode("utf-8"))
    assert result.status_code == 401
    assert result_json["code"] == Response_code.LOGIN_FAILED


def test_signup_success(client):
    result = client.post(
        "/signup",
        data=json.dumps(
            {
                "id": "testid",
                "pw": "testpw",
                "name": "testname",
                "email": "testemail@testemail.com"
            }
        ),
        content_type="application/json"
    )
    result_json = json.loads(result.data.decode("utf-8"))
    assert result.status_code == 200
    assert result_json["code"] == Response_code.SIGNUP_SUCCESS

    result = client.post(
        "/login",
        data=json.dumps({"id": "testid", "pw": "testpw"}),
        content_type="application/json"
    )
    result_json = json.loads(result.data.decode("utf-8"))
    assert result.status_code == 200
    assert result_json["code"] == Response_code.LOGIN_SUCCESS


def test_signup_failed(client):
    result = client.post(
        "/signup",
        data=json.dumps(
            {
                "id": "testid",
                "pw": "testpw",
                "name": "testname",
                "email": "testemail@testemail.com"
            }
        ),
        content_type="application/json"
    )
    result_json = json.loads(result.data.decode("utf-8"))
    assert result.status_code == 409
    assert result_json["code"] == Response_code.SIGNUP_FAILED


def test_addstamp(client):
    login_result = client.post(
        "/login",
        data=json.dumps(
            {
                "id": "testid",
                "pw": "testpw"
            }
        ),
        content_type="application/json"
    )
    login_result_json = json.loads(login_result.data.decode("utf-8"))

    assert login_result.status_code == 200
    assert login_result_json["code"] == Response_code.LOGIN_SUCCESS

    access_token = login_result_json["access_token"]

    add_result = client.post(
        "/addstamp",
        headers={"Authorization": access_token},
        data=json.dumps(
            {
                "memo": "superdupermemo"
            }
        ),
        content_type="application/json"
    )

    add_result_json = json.loads(add_result.data.decode("utf-8"))

    assert add_result.status_code == 200
    assert add_result_json["code"] == Response_code.ADD_STAMP_SUCCESS

    add_result = client.post(
        "/addstamp",
        headers={"Authorization": access_token},
        data=json.dumps(
            {
                "memo": "superdupermemo"
            }
        ),
        content_type="application/json"
    )

    add_result_json = json.loads(add_result.data.decode("utf-8"))

    assert add_result.status_code == 200
    assert add_result_json["code"] == Response_code.ADD_STAMP_ALREADY


def test_loadstamp(client):
    login_result = client.post(
        "/login",
        data=json.dumps(
            {
                "id": "testid",
                "pw": "testpw"
            }
        ),
        content_type="application/json"
    )
    login_result_json = json.loads(login_result.data.decode("utf-8"))

    assert login_result.status_code == 200
    assert login_result_json["code"] == Response_code.LOGIN_SUCCESS

    access_token = login_result_json["access_token"]

    load_result = client.post(
        "/loadstamp",
        headers={"Authorization": access_token},
        data=json.dumps(
            {
                "page": 0  # 0이면 가장 마지막 스탬프들을 가져옴
            }
        ),
        content_type="application/json"
    )

    load_result_json = json.loads(load_result.data.decode("utf-8"))
    print(load_result_json["response_data"])

    assert load_result.status_code == 200
    assert load_result_json["code"] == Response_code.LOAD_STAMP_SUCCESS
    assert load_result_json["response_data"]["stamp_list"][0]["memo"] == "superdupermemo"


def test_deletestamp(client):
    login_result = client.post(
        "/login",
        data=json.dumps(
            {
                "id": "testid",
                "pw": "testpw"
            }
        ),
        content_type="application/json"
    )
    login_result_json = json.loads(login_result.data.decode("utf-8"))

    assert login_result.status_code == 200
    assert login_result_json["code"] == Response_code.LOGIN_SUCCESS

    access_token = login_result_json["access_token"]

    load_result = client.post(
        "/deletestamp",
        headers={"Authorization": access_token},
        data=json.dumps(
            {
                "idxs": 1
            }
        ),
        content_type="application/json"
    )

    load_result_json = json.loads(load_result.data.decode("utf-8"))

    assert load_result.status_code == 200
    assert load_result_json["code"] == Response_code.DELETE_STAMP_SUCCESS


def test_removetesetid(client):
    result = client.post(
        "/removetestid",
        data=json.dumps(
            {
                "keycode": "superduperfantastickeycode"
            }
        ),
        content_type="application/json"
    )

    result_json = json.loads(result.data.decode("utf-8"))

    assert result.status_code == 200
    assert result_json["code"] == Response_code.TEST_ID_REMOVED

    login_result = client.post(
        "/login",
        data=json.dumps({"id": "testid", "pw": "testpw"}),
        content_type="application/json"
    )
    login_result_json = json.loads(login_result.data.decode("utf-8"))
    assert login_result.status_code == 401
    assert login_result_json["code"] == Response_code.LOGIN_FAILED
