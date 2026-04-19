#include <iostream>
#include <cstdlib>
#include<memory>
#include<vector>
#include<algorithm>
using namespace std;

int main()
{
    vector<string> sv;
    string name;

    cout<<"이름을 5개 입력하라"<<endl;
    for(int i=0; i<5;i++){
        cout << i+1<<">>";
        getline(cin,name);
        sv.push_back(name);
    }

    sort(sv.begin(), sv.end()); 
    for(string s :sv){
        
    cout<<"정렬 "<<s<<endl;
    }
    name = sv.at(0);
    for(int i=1;i<sv.size();i++){
        if(name<sv[i])name =sv[i]; 
    }
    cout<<"사전에서 가장 뒤에 나오는 이름은 "<<name<<endl;

    return 0;
}