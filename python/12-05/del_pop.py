list_a =[0,1,2,3,4,5]
print("# 리스트의 요소 하나 제거하기")

del list_a[1]#del로 지우기
print("del list_a[0]:",list_a)

list_a.pop(1)#()로 인덱스
print("pop list_a",list_a)

list_a.remove(3)#값으로 지움
print("remove",list_a)