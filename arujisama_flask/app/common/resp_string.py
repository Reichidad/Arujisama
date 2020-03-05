from .response_code import Response_code

ret_dict = {
    Response_code.DBFUNC_UNEXPECTED: "예기치 못한 오류",  # 이 부분은 쓸 일이 없어야함.
    # DB 쿼리 도중 오류,
    Response_code.DB_ERROR: "쿼리 도중 오류",
    # response 생성시 기본 값,
    Response_code.NONE: " --- ",  # 이 부분은 쓸 일이 없어야함.
    # idexistcheck,
    Response_code.ID_NOT_EXIST: "해당 ID가 없음.",
    Response_code.ID_EXIST: "해당 ID가 이미 있음.",
    Response_code.ID_MORE_THAN_ONE: "해당 ID가 2개 이상",  # 이 부분은 쓸 일이 없어야함.
    # id 글자수 검사,
    Response_code.ID_LENGTH_LIMIT_FAIL: "ID는 2자 이상, 20자 이하이어야 합니다.",
    # login,
    Response_code.LOGIN_SUCCESS: "로그인 성공",
    Response_code.LOGIN_FAILED: "로그인 실패. ID/PW를 확인해주세요.",
    # signup,
    Response_code.SIGNUP_FAILED: "가입 실패",
    Response_code.SIGNUP_SUCCESS: "가입 성공",
    # token,
    Response_code.TOKEN_VALID: "유효한 토큰",
    Response_code.TOKEN_INVALID: "유효하지 않은 토큰",
    # removetestid
    Response_code.TEST_ID_REMOVED: "테스트 아이디 제거 성공",
    Response_code.TEST_ID_REMOVE_ERROR: "테스트 아이디 제거 중 오류 발생",
    # loadstamp
    Response_code.LOAD_STAMP_SUCCESS: "스탬프 불러오기 성공",
    Response_code.LOAD_STAMP_FAILED: "스탬프 불러오기 실패",
    # addstamp
    Response_code.ADD_STAMP_SUCCESS: "스탬프 찍기 성공",
    Response_code.ADD_STAMP_FAILED: "스탬프 찍기 실패",
    Response_code.ADD_STAMP_ALREADY: "오늘은 이미 찍었음",
    # delete_stamp
    Response_code.DELETE_STAMP_SUCCESS: "스탬프 삭제 성공",
    Response_code.DELETE_STAMP_FAILED: "스탬프 삭제 실패",
    # validate_id
    Response_code.VALIDATE_ID_SUCCESS: "이메일 인증 성공",
    Response_code.VALIDATE_ID_FAILED: "이메일 인증 실패",
    # email 전송
    Response_code.SEND_VALIDATE_EMAIL_SUCCESS: "인증 이메일 전송 성공",
    Response_code.SEND_VALIDATE_EMAIL_FAILED: "인증 이메일 전송 실패",
    # 아직 인증되지 않은 ID로 로그인 시도한 경우
    Response_code.LOGIN_NOT_VALIDATED_ID: "아직 인증되지 않은 ID입니다.",
    Response_code.ALREADY_VALIDATED_ID: "이미 인증된 ID입니다.",
    # edit_stamp
    Response_code.EDIT_STAMP_SUCCESS: "스탬프 수정 성공",
    Response_code.EDIT_STAMP_FAILED: "스탬프 수정 실패",
    Response_code.EDIT_STAMP_NOT_MOST_RECENT: "최신 스탬프가 아닙니다",
    # find_id
    Response_code.FIND_ID_SUCCESS: "ID 찾기 성공",
    Response_code.FIND_ID_FAILED: "ID 찾기 실패",
    # find_pw
    Response_code.FIND_PW_SUCCESS: "PW 찾기 성공",
    Response_code.FIND_PW_FAILED: "PW 찾기 실패",
    # reset_pw
    Response_code.RESET_PW_SUCCESS: "비밀번호 초기화 성공",
    Response_code.RESET_PW_FAILED: "비밀번호 초기화 실패",
    Response_code.RESET_PW_EXPIRED: "만료된 초기화 링크",
    # 비밀번호 초기화 메일
    Response_code.RESET_PW_MAIL_SUCCESS: "비밀번호 초기화 이메일 전송 성공",
    Response_code.RESET_PW_MAIL_FAILED: "비밀번호 초기화 이메일 전송 실패"
}


def response_string(code):
    # dbfunc에서 발생하는 예기치 못한 오류
    return ret_dict.get(code, "정보 없음")
