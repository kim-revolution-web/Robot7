class Student:
    count =0
    student =[]

    @classmethod
    def print(cls):
        print("--- 학생 목록 ---")
        print("이름\t총점\t평균")
        for student in cls.student:
            print(str(student))
        print("--- --- ---")
    
    def __init__(self,name,korean,math,english,science):
        self.name =name
        self.korean=korean
        self.math=math
        self.english=english
        self.science = science
        Student.count+=1
        Student.student.append(self) # 이건 뭐지?

    def get_sum(self):
        return self.korean+self.math+\
        self.english+self.science
    
    def get_average(self):
        return self.get_sum()/4
    
    def __str__(self): 
        return "{}\t{}\t{}".format(\
            self.name,\
            self.get_sum(),\
            self.get_average())

Student("윤인성",87,98,88,98)
Student("연하진",87,98,88,98)
Student("구지연",87,98,88,98)
Student("나선주",87,98,88,98)
Student("김미화",87,98,88,98)
Student("박아현",87,98,88,98)
Student("서준서",87,98,88,98)
Student("박아현",87,98,88,98)
Student("서준서",87,98,88,98)

Student.print() #str이 있어서 나오는거야?
    