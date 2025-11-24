#include <iostream>
#include <cstdlib>
#include<memory>
#include<vector>
#include<list>
using namespace std;


int main()
{ vector<int> vec;

    vec.push_back(1);
    vec.push_back(2);
    vec.push_back(3);

    cout<<vec.size()<<endl;
    for(int i=0;i<vec.size();i++)
    cout<<vec[i]<<" ";
    cout<<endl;

    vec[0]=10;
    vec.at(1)=20;
    for(int i=0;i<vec.size();i++)
    cout<<vec[i]<<" ";
    cout<<endl;




    return 0;
}