list_a=[0,1,2,3,4,5]
print("# 리스트의 요소 하나 제거하기\n")

del list_a[1]
print("del list_a[1]:\n",list_a)
list_a.pop(2)
print(list_a)

for i in list_a:
 print(i,end=" ")
 print('\n')
 listb=[[1,2,3],[2,3,4],[5,6,8]]
 for item in listb:
  print(item)