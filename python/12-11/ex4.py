def test(fuction):
  def wrapper():
    print('인사가 시작되었습니다.')
    fuction()
    print('인사가 종료되었습니다.')
  return wrapper

#python에서 데코 레이터는 동작을 한다 
@test
def hello():
    print("hello")

#######################
hello()

