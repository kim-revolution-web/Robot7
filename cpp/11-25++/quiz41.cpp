#include <iostream>
#include <cstdlib>
#include<memory>
#include<vector>
#include<string>
#include<algorithm>

using namespace std;

//1 ~ 20까지 정수가 들어있는 vector 변수가 있다. 
//람다 표현식을 사용해서 벡터에서 홀수만 출력 봅니다.
int main()
{
    vector<int> vec;
    //1.혹시 원소들 값이 정렬 되어 있지 않다면
    for(int i=1;i<21;i++){
        vec.push_back(i);
        }
    

    for_each(vec.begin(),vec.end(),
[](int n){
    if(n%2==1){
        cout <<n<<" ";
    }

});
 cout<<endl;
    

    return 0;
}