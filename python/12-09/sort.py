numbers=[103,52,273,32,77]

print(min(numbers))
print(max(numbers))
numbers.sort()
print(numbers)
alist =list(reversed(numbers))
print(alist)

for i in reversed(numbers):
    print(i)

print("sort 안에 속성값")
numbers.sort(reverse=False)
print(numbers)

numbers.sort(reverse=True)
print(numbers)