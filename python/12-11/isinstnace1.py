class Human:
    def __init__(self):
        pass
class Student(Human):
    def __init__(self):
        pass

student= Student()

print("isinstance(student,Human):",isinstance(student,Human))
print("type(student)==Human:",type(student)==Human)