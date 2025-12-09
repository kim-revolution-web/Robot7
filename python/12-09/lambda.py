def call_10_times(func): #매개변수에 사용되는 함수 --> 콜백함수
    for i in range(10):
        func()

def print_hello():
    print("안녕하세요")

call_10_times(print_hello)
