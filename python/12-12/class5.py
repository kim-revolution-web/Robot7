import math

class circle:
    def __init__(self,radius=5):
        self.__radius=radius
    
    @property
    def radius(self):
        return self.__radius
    @radius.setter #매소드는 변수랑 다르게 뭔가 할수 있다?
    def radius(self,value):
        if value<=0:
            raise TypeError('길이는 양의 숫자여야 합니다.')
        self.__radius=value
    

if __name__ == "__main__":
    circle = circle()
    #circle.__radius =7 #에러감
    circle.radius = 8
    print(circle.radius)