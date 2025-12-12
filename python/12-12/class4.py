import math

class circle:
    def __init__(self,radius=5):
        self.__radius=radius
    
    def getReadius(self):
        #보안, 암호화, 복화화,로그
        return self.__radius

    def setReadius(self,radius):
        #보안, 암호화, 복화화,로그
         self.__radius=radius

if __name__ == "__main__":
    circle = circle()
    #circle.__radius =7 #에러감
    circle.setReadius(7)
    print(circle.getReadius())