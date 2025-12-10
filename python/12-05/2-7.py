number = input("정수 입력>")
last_character= number[-1]
print(last_character)

if last_character in "02468":
    print("짝수입니다")

if last_character in "13579":
    print("홀수입니다")

number = int(input("정수 입력>"))

if number%2==0:
    print("짝수입니다")
if number%2==1:
    print("홍수입니다")
    