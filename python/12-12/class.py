class Student:
    def __init__(self,id=0,name="청수",pnumber="없음"):
        self.__id = id
        self.__name=name
        self.__pnumber=pnumber
    def study(self):
        print("공부를 합니다.")

    def __str__(self):
        return "{}/{}/{}".format(self.__id,self.__name,self.__pnumber)

    def setter_id(self,id):
        self.__id=int(id)
    def setter_name(self,name):
        self.__name=str(name)
    def setter_pnumber(self,pnumber):
        self.__pnumber=str(pnumber)

    def getter_id(self):
       return self.__id
    def getter_name(self):
       return self.__name
    def getter_pnumber(self):
       return self.__pnumber

minsu = Student(1,"민수","010-1234-1234")
minsu.study()
print(minsu.getter_name())
print(minsu)