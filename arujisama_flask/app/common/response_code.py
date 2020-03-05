import enum


class Response_code(enum.IntEnum):
    # dbfunc에서 발생하는 예기치 못한 오류
    DBFUNC_UNEXPECTED = -98
    # DB 쿼리 도중 오류
    DB_ERROR = -99
    # response 생성시 기본 값
    NONE = 0
    # id_exist_check
    ID_NOT_EXIST = 1
    ID_EXIST = 2
    ID_MORE_THAN_ONE = 3  # 이 부분은 쓸 일이 없어야함.
    # id 글자수 검사
    ID_LENGTH_LIMIT_FAIL = 4
    # login
    LOGIN_SUCCESS = 5
    LOGIN_FAILED = 6
    # sign_up
    SIGNUP_FAILED = 7
    SIGNUP_SUCCESS = 8
    # token
    TOKEN_VALID = 9
    TOKEN_INVALID = 10
    # remove_testid
    TEST_ID_REMOVED = 11
    TEST_ID_REMOVE_ERROR = 12
    # load_stamp
    LOAD_STAMP_SUCCESS = 13
    LOAD_STAMP_FAILED = 14
    # add_stamp
    ADD_STAMP_SUCCESS = 15
    ADD_STAMP_ALREADY = 16
    ADD_STAMP_FAILED = 17
    # delete_stamp
    DELETE_STAMP_SUCCESS = 18
    DELETE_STAMP_FAILED = 19
    # validate_id
    VALIDATE_ID_SUCCESS = 20
    VALIDATE_ID_FAILED = 21
    # email 전송
    SEND_VALIDATE_EMAIL_SUCCESS = 22
    SEND_VALIDATE_EMAIL_FAILED = 23
    # 아직 이메일 인증 되지 않은 ID로 로그인 시도한 경우
    LOGIN_NOT_VALIDATED_ID = 24
    # 이미 이메일 인증된 ID의 링크에 재접속 한 경우
    ALREADY_VALIDATED_ID = 25
    # edit_stamp
    EDIT_STAMP_SUCCESS = 26
    EDIT_STAMP_FAILED = 27
    EDIT_STAMP_NOT_MOST_RECENT = 28
    # find_id
    FIND_ID_SUCCESS = 29
    FIND_ID_FAILED = 30
    # find_pw
    FIND_PW_SUCCESS = 31
    FIND_PW_FAILED = 32
    # reset_pw
    RESET_PW_SUCCESS = 33
    RESET_PW_FAILED = 34
    RESET_PW_EXPIRED = 35
    # 비밀번호 초기화 메일
    RESET_PW_MAIL_SUCCESS = 36
    RESET_PW_MAIL_FAILED = 37
