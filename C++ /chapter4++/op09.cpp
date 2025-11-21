#include <iostream>
#include <cstdlib>
using namespace std;

int main()
{
    int* p;

    p= new int[5];

    for(int i=0;i<5;i++){
        p[i]=i+1;///1 23 34 5 
        cout<< p[i]<<endl;

    }
    delete [] p;

    return 0;
}