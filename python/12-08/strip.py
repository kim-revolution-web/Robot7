a="""                   안녕하세요
문자열의 함수를 알아봅니다
1234234
           abcdefg
"""
 

print(a)
print(a.strip())

print(a.isalnum())
print(a.isalpha())
print(a.isidentifier())
print(a.isdecimal())
print(a.isdigit())
print(a.isspace())
print(a.islower())

abc="안녕하세요 파이썬"
print(abc.find("안녕"))
print(abc.rfind("안녕"))

s = "안녕 파이썬 안녕"

print(s.find("안녕"))   # 0      (앞에서 찾은 첫 번째)
print(s.rfind("안녕"))  # 8 같은 값 (뒤에서 찾은 첫 번째)