#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

double squre(double a){
    return a*a;
}
float squre(float a){
    return a*a;

}


int main()
{
    cout<<squre(3.0)<<endl;
    cout<<squre(3)<<endl;
    return 0;
}