class Student:
    def __init__(self,name,korean,math,english,science):
        self.name = name #self.name 변수선언하고 name 을 넣은거
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science
Students = [
    Student("윤인성",87,98,88,95),
    Student("연하진",92,98,96,98),
    Student("구지연",87,96,94,90),
    Student("나선주",98,92,96,92),
    Student("윤아린",95,98,98,98),
    Student("윤명월",98,92,96,92),
]
for person in Students:
    print("{},{},{},{},{}".format(person.name,person.korean,
                                  person.math,person.english,person.science))
