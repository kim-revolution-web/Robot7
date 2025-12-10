array =[]

for i in range(0,20,2):
    array.append(i*i)
print(array)

array = [i*i for i in range(0,20,2)]

print(array)

words = ["apple","kiwi","banana","grap","pear"]

long_word = [w for w in words if len(w)>=5]
print(long_word)