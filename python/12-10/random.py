import random
import os

base_dir = os.path.dirname(__file__)    
path = os.path.join(base_dir, "basic.csv")

hanguls =list("가나다라마바사아자차카타파하")
         
 
with open(path, "w", encoding="utf-8")as f:
    for i in range(1000):
        name= random.choice(hanguls)+random.choice(hanguls)+random.choice(hanguls)
        weight=random.randrange(40,140)
        height=random.randrange(140,230)

        f.write("{},{},{}\n".format(name,weight,height))