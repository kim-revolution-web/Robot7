numbers=[1,2,6,8,2,3,4,7,6,8,9,1,4,4,2,3,]
counter={}
for number in numbers:
  if number in counter:
     counter[number]+=1
  else:
     counter[number]=1
     
print(counter)
 