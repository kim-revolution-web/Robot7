
try:
    with open("abc.txt","r") as f:
        text= f.reaf()
except:
    print('파일이 경로에 없습니다.')

else :
    print("정상적이라면 여기에 코드 실행")
finally:
    print("프로그램을 안전하세 종료 합니다")


