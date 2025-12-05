list_a=[[1,2,3],[4,5,6],[7,8,9]]
print(list_a[2])
print(list_a[1][1])
print(list_a[0][:])

print("b만")
list_b=[1,2,3]
print(list_b)
list_c=list_b
print("#얕은 복사")
list_b[0]=100
print(list_b)
print(list_c)
print("#깊은 복사 list_d")
list_d=list(list_b)
list_b[0]=200
print(list_b)
print(list_c)
print(list_d)
print("////////////////")
import copy
list_e=copy.deepcopy(list_b)
list_b[0]=300

print(list_b)
print(list_c)
print(list_e)



