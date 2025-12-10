import random
astudent=list("김이박최정강조윤장임")
bstudent=list("기정나다영민송정한고연영")

with open("students.csv","w")as file:
  for i in range(0,30,1):
        id= random.randrange(1,31)
        name= random.choice(astudent)+random.choice(bstudent)+random.choice(bstudent)
        math= random.randrange(0,101)
        english= random.randrange(0,101)
        file.write("{},{},{},{}\n".format(id,name,math,english))

