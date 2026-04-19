#include <iostream>
#include <cstdlib>
#include<memory>
#include<string>
#include<map>

using namespace std;

int main()
{ map<string,string> dic;

    dic.insert(make_pair("love","사랑"));
    dic.insert(make_pair("apple","사과"));
    dic["cherry"]="체리";

    cout <<"저장된 단어개수"<<dic.size()<<endl;

    string eng;
    while(true){
        cout<<"찾고 싶은 단어>>";
        getline(cin,eng);
        if(eng=="exit")break;

        if(dic.find(eng)==dic.end()) //“끝 위치와 같다 = 어디에서도 못 찾았다” 라는 의미.
        cout<<"없음"<<endl;
        else
        cout <<dic[eng]<<endl;
    }
    cout<<"종료 합니다.."<<endl;

    return 0;
}