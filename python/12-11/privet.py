class Person:
    def __init__(self,name):
        self.__name = name #privete
        # _ 언더바 한개는 protected 언더바 두개는 private, 없으면 public

        #getter
    def getName(self):
        return self.__name    
    #setter
    def setName(self,name):
        self.__name=name

soonsin = Person("이순신")
print(soonsin.getName())

soonsin.setName("강감찬")
print(soonsin.getName())