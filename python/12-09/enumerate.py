example_list = ["요소A","요소B","요소C"]

print("# 단순 출력")
print(example_list)
print()

print("enumerate()함수를 적용해 출력합니다.")

print(enumerate(example_list))
print()

print("#list () 함수로 강제 변환 출력")
alist=list(enumerate(example_list))
print(alist)
print(alist[1])
print(type(alist))
print(type(alist[0])) #tuple

print("튜플 리스트 출력하기")
for index, value in enumerate(example_list):
    print("{}번째 요소는 {}입니다.".format(index,value))

