# 2. 문제 2: 문자열 리스트에서 길이가 5 이상인 단어의 길이만 뽑아내기
# 다음 문자열 리스트가 있다.

# words = ["python", "map", "filter", "lambda", "hi", "education", "code"]
# 조건

# filter로 길이가 5 이상인 단어만 남겨라.

# map으로 각 단어의 문자 개수(len) 를 구하는 리스트를 만들라.

# 결과를 리스트로 출력하라.
# 예상 출력 예시:

# [6, 6, 7, 9]

words = ["python", "map", "filter", "lambda", "hi", "education", "code"]

a=filter(lambda words: len(words)>4,words)

b=map(lambda a:len(a),a)
print(list(b))