#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

template<class T>
void mySwap(T &a, T &b)
{
    T tmp;
    tmp =a;
    a=b;
    b=tmp;
}
int main()
{
    double a=4.2,b=5.3;
    mySwap(a,b);

    cout<<"a는 :"<<a<<"b는"<<b<<endl;
    return 0;
}