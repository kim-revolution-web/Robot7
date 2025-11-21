#include <iostream>
#include <cstdlib>
using namespace std;

int main()
{
    int i,sum=0;
    int *p;
    cout<<"입력하세요"<<endl;
cin>>i;

if(i<=0)return 1;

p=new int[i];

for(int n=0;n<i;n++){

    cout<<"더할 값입력"<<endl;
    
    cin>>p[n];
    sum +=p[n];
}


cout<<"sum :"<<sum<<endl;
delete [] p;
    return 0;
}