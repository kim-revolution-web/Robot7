#include <iostream>
#include <cstdlib>
#include<memory>
#include<string>
#include<algorithm> //reverse

using namespace std;

int main()
{
    int n=0;
    string str="";
    getline(cin,str);

    // for(string s:str){ for문 범위 가능?
    // }
    //for(char ch:str)

    //for(int i=0;i<str.length();i++) n++; //str.size

        n=str.length();

    for(n=n-1;n>=0;n--){
        //cout<<str[n];
        cout<<str.at(n);
    }
    cout<<endl; //줄바꿈
    return 0;
}