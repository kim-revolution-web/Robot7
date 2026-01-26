
def main1(): 
    n = list(map(int,input().split()))
   #map은 리스트(또는 반복 가능한 값들)의 각 요소에 int()를 적용해줘서
    #문자열들을 숫자로 바꿔주는 걸 “도와주는” 역할이야. 
    max=n[0]
    for i in range(1,len(n)): #len(n) 이면 n의 길이n-1까지 나오는거아니야?
        if n[i]>max:
            max=n[i]
    print(max)
#for x in n[1:]: 이것도 끝까지 비교해줘

def main2():
    s = input()
    s= list(map(int,s.split()))
    n=s[::-1]
    for i in n[0:]:
        print("main2",i)


if __name__ == "__main__":
    main2()