#filter(function,list),map(lamda,list)
# 1. 문제 1: 짝수만 골라 제곱 리스트 만들기
# 다음 리스트가 있다.

# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 조건

# filter를 사용하여 '짝수'만 걸러라.

# map을 사용하여 '걸러진 값의 제곱'을 계산하라.

# 최종 결과 리스트를 출력하라.

# 예상 출력 형태:

# [4, 16, 36, 64, 100]
numbers=[1,2,3,4,5,6,7,8,9,10]

def v(x):
    return x%2 == 0

a=filter(lambda x: x%2==0,numbers) #객체
b=list(a)
# print(b)

c=map(lambda x: x*x,b)
print(c)
#print(list(c))
