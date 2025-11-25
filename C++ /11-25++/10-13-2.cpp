#include <iostream>
#include<vector>
using namespace std;


int main()
{
    vector<char>vec={'A','B','C'};

    vector<char>::iterator it;

    for(it=vec.begin();it!=vec.end();it++){

        cout << *it <<" ";
    }
    cout<<endl;

    
    return 0;
}