dictionary={
    "name":"7D 건조 망고",
    "type":"당절임",
    "ingredient":["망고","설탕","메타중아황산나트륨","치자황색소"],
    "origin":"필리핀"
}
d=dictionary
v=d.get("존재하지 않는 키")
print(v)
#print(d.get("type"))

for key in d:
    print(key,":",d[key])
print(d)