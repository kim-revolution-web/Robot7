import time

number =0

target_tick = time.time() +2

while time.time()<target_tick:
    number +=1

print('2초 동안 {}번 반복 했습니다.'.format(number))