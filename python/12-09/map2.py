numbers = [1,2,3,4,5]

# def is_even(x):
#  return x%2 ==0

# result = filter(is_even,numbers)
result= filter(lambda x: x%2 !=0,numbers)

print(list(result))
