### Python 3.7 및 파이참(PyCharm)을 깔고 진행해주세요
##### 윈도우 기준으로 작성되었습니다.
<br/>
이 레포를 pull 받았다면 flask와 관련해서 다음을 진행해주세요.<br/>
<br/>
1. .gitignore 설정하기<br/>
 - arujisama_flask/.idea <br/>
 - arujisama_flask/venv <br/>
 - arujisama_flask/app/__pycache__/ <br/>
이 3개는 직접적인 소스코드가 아니므로 공유가 될 필요 없는 폴더들입니다. <br/>
<br/>
2. 받아온 레포를 Pycharm에서 불러온다. <br/>
 - 프로젝트를 새로 만들지 말고, open으로 불러옵니다. <br/>
 - 불러올 때, arujisama의 root폴더가 아닌, arujisama_flask 폴더를 불러오도록 합니다. <br/>
 - 불러왔으면 Ctrl + Alt + S를 누릅니다. (Settings를 엽니다.) <br/>
 - 왼쪽에 Project:~~~ 가 있을 텐데 그 옆의 > 를 누른 후 Project Interpreter 메뉴 선택 <br/>
 - Project Interpreter 맨 오른쪽에 설정 아이콘 -> Add 클릭 (이미 설정되어 있어도, 가상환경 다시 만들어야함!) <br/>
 - 가상환경 설정이 뜰 텐데, New Environment 선택. Base Interpreter는 Python 3.7. (미리 깔아놓아야 Python 3.7이 표시됨) <br/>
 - 작업이 끝나고 pip와 setuptools가 뜨면 완료. OK 버튼을 눌러서 나온다. <br/>
 - 파이참을 한 번 재시작해준다. <br/> 
 - 파이참 왼쪽 아래에서 2번째 줄에 Terminal이라는 메뉴가 있을텐데 클릭. <br/>
 - 콘솔창이 뜬다. "pip install -r requirements.txt"라고 입력 후 엔터 <br/>
 - 머라머라 뜨면서 설치됨. <br/>
 - 그럼 이제 run.py를 열고, 메뉴에서 Run -> Run...(Alt + Shift + F10) 메뉴를 선택한 후 run을 실행해보자. <br/>
 - Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)라고 뜬다면 정상적으로 설치가 완료된 것. <br/>
 - 아무 인터넷 브라우저나 켠 후 주소창에 127.0.0.1:8080이라 입력한 후 엔터 <br/>
 - 빈 화면에 Hello! 라고 뜬다면 끝 <br/>
 <br/>
2019-07-23 작성
 * * *
