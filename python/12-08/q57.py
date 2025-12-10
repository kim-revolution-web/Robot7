nums=[1,3,5,7]
for i in nums:
    for j in nums:
     #print('({},{})'.format(i,j))
     print (f'({i},{j})')

array={
   [1,2,3]
   [4,5,6]
   [7,8,9]
}

sum =0
for i in array:
    for j in i:
      sum+=j

      print("요소의 합",sum)