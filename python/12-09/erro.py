
#def print_n_times(n=2,*values): 가변매개 변수 보다 일반 변수가 올수 없다 
#뒤에서 써야 가변,기본변수 형이 된다

def print_n_times(*values,n=2):

    for i in range(n):
        for value in values:
            print(value)
        print()


print_n_times("안녕하세요","즐거운","파이썬 프로그래밍",n=3)