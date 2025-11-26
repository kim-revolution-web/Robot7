#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

char & find (char s[],int index){return s[index];}
int main()
{
    char name[]="Mike";
    cout<<name<<endl<<endl;

    //name[0] ='S';
    find(name,0)='S';
    cout<<name <<endl;

    char&ref = find(name,2);
    ref='t';
    cout<<name<<endl;//Site
    
    return 0;
}