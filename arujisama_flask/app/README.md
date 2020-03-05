### API 정리
##### API의 response code 관련 내용은 common.responsecode와 common.resp_string 참조

1. {url}/
- 루트 페이지. 현재는 templete/index.html을 띄우게 함
  
2. {url}/idexistcheck (아이디 중복검사)
 - 필요 패러미터 = { id : XXX }
 - user_login 테이블에서 id값이 XXX 와 중복되는 것이 있는 지 검사한다.
 - 동작은 dbfunc.idexistcheck 참조. 참고로 이 메소드 자체는 로그인과 회원가입에서도 사용함. 

 
3. {url}/login (로그인)
 - 필요 패러미터 = { id : XXX, pw : YYY}
 - user_login 테이블에서 id와 pw값이 일치하는 것이 있는지 검사한다.
 - 동작은 dbfunc.login 참조
 - pw값은 현재는 DB에서 받은 후 MD5 해쉬값으로 치환해서 검사함.
 - 브라우저에서 MD5 해쉬값을 넘겨주게 바꾸면 코드 반영 예정.

 
4. {url}/signup (회원가입)
 - 필요 패러미터 = { id : XXX, pw : YYY, name : ZZZ, email: aaa@bbb.ccc }
 - ID, PW, 이름, 이메일 형식 등은 일단 브라우저에서 검사를 다 마친 것으로 가정
 - 빈칸인지 여부만 확인하고 빈칸인 것이 있으면 되돌리고, 아니면 그대로 DB에 넣는다.
 - 동작은 dbfunc.signup 참조
