array = [273, 32, 103,"문자열", True,False]
print(array)
print(type(array))

array[0]="변경"
print(array)

print(array[-1])
print(array[3][0])
print(array[3][1])
print(array[3][2])
array[3]="12345"
print(array[3][3:])
print(array[3][1:3])