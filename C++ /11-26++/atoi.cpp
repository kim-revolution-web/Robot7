#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

int main()
{
    char* chs = "12345";
    string str = "12335";
    char number[100]="12355";

    cout<<"chs"<<stoi(chs)<<endl;
    cout<<"str"<<stoi(str)<<endl;
    cout<<"number"<<stoi(number)<<endl;

    return 0;
}