import urllib.request


target = urllib.request.urlopen('https://google.com')
output = target.read()

print(output)

from urllib import request
target = request.urlopen('https://google.com')  # 앞에 urllib. 빼기
output = target.read()
print(output)

# urllib
#     |--__init__py
#     |--__request.py
#     |--__parse.py
#     |--__error.py
#     |--__robotparser.py
#     |--__response.py
