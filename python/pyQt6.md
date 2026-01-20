
# ~/pyQt 디렉토리

# ln -s /mnt/c/Users/admin/Desktop/'인천 인재개발원'/pyQt6 ~/pyQt
ln 별명  
- s는 ln 명령에서 **심볼릭 링크(symbolic link) = “바로가기”**를 만들라는 옵션
~/pyQt 별명으로 이동

우분투 에서

Ubuntu에서 apt로 관리하는 파이썬/패키지랑 pip로 설치하는 패키지가 섞이면

- 업데이트 꼬임
- 의존성 충돌
- OS 패키지 깨짐
    
    이런 문제가 생겨서 **시스템 영역 설치를 차단**한 거야.
    

# 해결: venv 만들고 그 안에 pyQt6 설치 ✅

```bash
cd ~/work/pyQt6
sudo apt update
sudo apt install -y python3-venv
python3 -m venv .venv
```

- sudo **“관리자 권한으로 실행”**하는 명령어야.  
- apt 우분투(리눅스) 프로그램 설치/업데이트 도구야. (패키지 관리자)
- 관리자 권한으로 python3-venv 패키지를 설치

- python3 -m venv .venv
- -y는 “중간에 ‘계속할까요?’ 물어보면 자동으로 Yes”라는 뜻.
  
- 현재 폴더 안에 .venv라는 폴더를 만들고, 그 안에 전용 파이썬/라이브러리 공간을 세팅한다는 의미
- python3 -m venv .venv를 실행하면 파이썬이 .venv 폴더를 스스로 만들고 그 안에 가상환경 파일들을 채워 넣어.


```bash
source .venv/bin/activate
python -m pip install -U pip
python -m pip install PyQt6
```

- source는 그 스크립트를 “현재 터미널(현재 쉘)”에서 실행하게 해주는 명령이야.
- .venv/ : 가상환경 폴더
- bin/ : 실행 파일/스크립트들이 들어있는 폴더
- activate : “이 가상환경을 현재 터미널에 적용”해주는 스크립트 파일


```bash
왜 “현재 터미널”이 중요하냐면, activate는 실행하면서
PATH를 바꿔서 .venv/bin이 우선되게 하고
VIRTUAL_ENV 같은 환경변수를 세팅하고
프롬프트 앞에 (.venv) 표시가 뜨게 하거든
그래서 그냥 실행(./activate)하면 “별도 프로세스”로 돌아가서 효과가 남지 않는데, source로 해야 내 터미널이 바뀜.
잘 되면 프롬프트가 (.venv) admin1@...$ 처럼 바뀜
끄고 싶으면 deactivate
```

- m이 뭐야?
- python -m pip는 “pip라는 모듈을 현재 파이썬으로 실행해라”라는 뜻이야.
- 이걸 쓰는 이유:
- pip만 치면 다른 파이썬의 pip가 잡힐 때가 있는데,
- python -m pip는 지금 선택된 python(특히 가상환경의 python) 에 딱 맞는 pip를 실행해줌.


- U는 뭐야?
- U는 --upgrade의 줄임말.
- 이미 설치된 pip가 있으면 최신 버전으로 업그레이드 해.


```bash
sudo apt update
sudo apt install -y qttools5-dev-tools
```
- sudo apt update=“목록 갱신”
- 실제로 시스템 업그레이드는 sudo apt upgrade임
이건 “Qt5 개발 도구들(툴 모음)” 패키지야.
PyQt6을 설치하는 것 자체랑은 별개인데, Qt 관련 유틸리티가 필요할 때 설치하는 경우가 있어.


```bash
이 안에 대표적으로 들어가는 게:
Designer(디자이너): 버튼/창을 드래그로 배치해서 .ui 파일 만드는 GUI 툴
assistant, linguist 같은 Qt 개발용 도구들
uic 같은 UI 변환 도구(환경에 따라)
```

- PyQt6 = 파이썬에서 Qt GUI 만들기 라이브러리
- Qt tools = Qt를 개발할 때 쓰는 “외부 도구(프로그램)”들

<img width="836" height="342" alt="image" src="https://github.com/user-attachments/assets/8f1ce690-14d1-4c19-a15d-30f049250b9f" />
<img width="795" height="490" alt="image" src="https://github.com/user-attachments/assets/db857f19-a9a0-47f4-9630-acad003a534c" />
<img width="831" height="279" alt="image" src="https://github.com/user-attachments/assets/11605c9b-5982-4b26-a5be-c5813c018996" />  
인터프리터 경로 입력에 주소입력



