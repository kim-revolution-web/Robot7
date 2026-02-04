from pathlib import Path

def main1(): #1) 홀짝 판별
    n = list(map(int,input().split()))
    for i in n:
     print(f"{i}:{'EVEN' if i%2==0 else 'ODD'}")

def main2(): #2) 1부터 n까지 합
    n = int(input())
    total = 0
    for i in range(1,n+1):#for에는 list 만들어감
        total+=i
    print(total) 

def main2_1():
    n = list(map(int,input().split()))
    total = 0
    for i in n:
        total+=i
    print(total)

def main3(): #3) 리스트에서 최댓값 찾기
    n = list(map(int,input().split()))
    max = n[0]
    for i in n[1:]:
        if i > max:
            max=i
    print(max)

def main4(): #4) 문자열 뒤집기
    n = list(map(int,input().split()))
    # rev=n[::-1]
    # for i in rev:
    #     print(i)
    print(n[::-1])
    m = input()
    print(m[::-1])

    
def main4_1(): 
    s = input()
    #s str
    
    for i in s[::-1]:
        print(i)

def main5(): #5) 단어 개수 세기
    line  = input()
    print(len(line.split()))

def main6(): #6) 구구단 2단~9단 출력
    for dan in range(2,10):
        for i in range(1,10):
            print(f"{dan}*{i} ={dan*i}")

def main7(): #7) 함수로 평균 구하기
 while True: 
    try:
     nums=list(map(int,input().split()))
    except ValueError:
        print(f"다시 입력")
        continue 
    else:      
     print(f"{sum(nums) / len(nums) if nums else 0}")
     break

def main8(): #8) 딕셔너리로 빈도수 세기
    s = input()
    freq={}
    for i in s:
            if i == ' ' :
                continue
            freq[i] = freq.get(i, 0) + 1
    for k,v in freq.items():
      print(k,v) 

def main9(): #9소수 판별
    n = int(input())
   
    if n>2:
        for i in range(2,n):
            k=0
            if n%i==0:
                k+=1
                print(f"소수가 아니다")
                break
        if k!=1:
            print(f"소수임")

def main9_1():
    n = int(input())
    if n>2:
        for i in range(2,int(n ** 0.5)+1):
            if n%i==0:
                print("소수가 아니다")
                return
        print(f"소수 이다")

def main10():  #10파일에 한줄 저장하기 
    text = input()
    here = Path(__file__).resolve().parent
    fpath = here / "momo.txt"
    with open(fpath,"a",encoding="utf-8")as f:
        f.write(text + "\n")

    with open(fpath, "r", encoding="utf-8") as f:
     data = f.read()
     print(data)



if __name__ == "__main__":
    main10()
    # import os
    # print(os.getcwd())