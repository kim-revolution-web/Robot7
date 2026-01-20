
# ~/pyQt 디렉토리

# ln -s /mnt/c/Users/admin/Desktop/'인천 인재개발원'/pyQt6 ~/pyQt
ln 별명  
-s는 ln 명령에서 **심볼릭 링크(symbolic link) = “바로가기”**를 만들라는 옵션
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

-sudo **“관리자 권한으로 실행”**하는 명령어야.  
-apt 우분투(리눅스) 프로그램 설치/업데이트 도구야. (패키지 관리자)

-python3 -m venv .venv
현재 폴더 안에 .venv라는 폴더를 만들고, 그 안에 전용 파이썬/라이브러리 공간을 세팅한다는 의미


```bash
source .venv/bin/activate
python -m pip install -U pip
python -m pip install PyQt6

```




