print("정수하나 입력")
a=int(input())
print("정수하나 입력")
b=int(input())
print("기호 입력")
c=input()

if(c=='+'):
    print({},a+b)

elif(c=='-'):
    print(a-b)

elif(c=='*'):
    print(a*b)

elif (c=='/'):{
 print(a/b)
}
else:print("입력이 잘못됬다")
    
if(a%3==0):{
    print("OK")
    
}
else:
    if(a%5==0):{
    print("OK")
    }
    else:
     print("NO")

    
   
