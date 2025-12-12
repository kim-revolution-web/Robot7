class Student:
    def __init__(self,id,name):
        self.__id =id
        self.__name =name
    
    @property
    def id(self):
        return self.__id
    @property
    def name(self):
        return self.__name
    
    @id.setter
    def id(self,id):
        self.__id =id

    @name.setter
    def name(self,name):
        self.__name =name

chulsoo = Student(1,"철수")

chulsoo.id =2
chulsoo.name ="철얼~쑤"

print(chulsoo.id,':',chulsoo.name)