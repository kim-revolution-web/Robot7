# file =open("basic.txt","w")
# # print(type(file))
# file.write("Hello Python Programming...!")

# file.close()

#with를 사용하여 close()를 호출
with open("basic.txt","w")as file:

    file.write("Hello Python Programming>>!")

with open("basic.txt","r")as file2:

   a= file2.read()
   print(a)