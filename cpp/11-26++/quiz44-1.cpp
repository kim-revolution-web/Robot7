#include <iostream>
#include <cstdlib>
#include<memory>
#include<vector>
#include<algorithm>
#include<list>

using namespace std;


int main()
{
    vector<string> vec;
    list<string> list;
    string name;
    
     
    for(int i=0;i<5;i++){
       getline(cin,name);
       vec.push_back(name);
       list.push_back(name);
    }

    sort(vec.begin(),vec.end());
    //sort(list.begin(),list.end());
    list.sort();//오름차순 list.sort(greater<string>())//내림차순

    cout<<vec.at(vec.size()-1)<<endl;
    cout<<list.back()<<endl;

   




    

    return 0;
}