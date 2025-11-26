#include <iostream>
#include <cstdlib>
#include<memory>
#include<vector>
#include<algorithm>


using namespace std;


int main()
{
    string names[5];
    for(int i=0;i<5;i++){
        cout<<"이름>>";
        getline(cin,names[i],'\n');
    }
   
    string laterr = names[0];
    for(int j=0;j<5;j++){
    if(laterr<names[j]){
        laterr=names[j];
    }
}
cout<<"사전에서 가장뒤에 나오는 문자열은"<<laterr<<endl;


    

    return 0;
}