#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

void msg(int id){
    cout<<id<<endl;}

void msg(int id,string s=""){
    cout<<id<<':'<<s<<endl;
}

int main()
{ msg(6);// 디폴트 매개 변수 --> 매개변수 2개를 사용한것 
    msg(5,"Good Morning");
    
    return 0;
}