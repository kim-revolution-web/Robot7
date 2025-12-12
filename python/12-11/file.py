import os
a=os.path.dirname(__file__)
b=os.path.join(a,"just.txt")

with open(b,"w")as filew:
    filew.write("안녕하세요\n반갑습니다\n")

with open(b,"r")as filer:
    c=filer.read()
    print(c)


print("변경 전:", os.getcwd())  # 현재 작업 디렉토리 확인

os.chdir("/home/robot/work/python1/12-11py")

print("변경 후:", os.getcwd())
with open("just.txt","r")as r:
    print(r.read())
   