import datetime #기본 제공 내부 모듈

now= datetime.datetime.now()

# print(now.year,"년")
# print(now.month,"월")
# print(now.day,"일")
# print(now.hour,"시간")
# print(now.minute,"분")
# print(now.second,"초")

print("{}년 {}월 {}일".format(now.year,now.month,now.day))
print(f"{now.year}년 {now.month}월 {now.day}일")