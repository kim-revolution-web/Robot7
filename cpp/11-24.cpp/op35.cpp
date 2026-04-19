#include <iostream>
#include <cstdlib>
#include<memory>
#include<vector>
#include<list>
using namespace std;

int main(){
    int sum=0;
    double avg=0;

    vector<int> vec;
    
    vec.push_back(3);
    vec.push_back(5);
    vec.push_back(8);
    
    for(int i= 0;i<vec.size();i++){
       sum+= vec[i];
       
    }
    avg=(double)sum/vec.size();
    cout<<"sum 총점"<<sum<<endl;
    cout<<"avg 총점"<< avg<<endl;


    return 0;
}