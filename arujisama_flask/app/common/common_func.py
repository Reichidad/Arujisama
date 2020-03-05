import os
import json

from .response_code import Response_code
from . import resp_string
from flask import make_response, jsonify, redirect


def generate_response(statuscode, code=Response_code.NONE, access_token=None, data=None):
    result_dict = {}
    if code != Response_code.NONE:
        result_dict['code'] = code
        result_dict['notation'] = resp_string.response_string(code)
    if access_token is not None:
        result_dict['access_token'] = access_token
    if data is not None:
        result_dict['response_data'] = data

    if len(result_dict) > 0:
        result = make_response(
            jsonify(
                result_dict
            )
            , statuscode
        )
    else:
        result = make_response(statuscode)

    return result


def get_cwd_directory(path=''):
    return str(os.getcwd()) + path


def get_secret_key():
    secret_key_file = get_cwd_directory('/app/config_files/secret_key.json')
    try:
        with open(secret_key_file, mode="r") as fp:
            line = json.load(fp)
            return line['secret_key']

    except FileNotFoundError as e:
        return FileNotFoundError


def generate_redirect(destination, access_token=None):
    result = redirect(destination)
    '''
    if access_token is not None:
        header = {"Authorization": access_token}
        result.headers = header
    '''
    return result
