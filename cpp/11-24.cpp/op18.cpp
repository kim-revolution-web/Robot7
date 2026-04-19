#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

class TV{
    protected:
    int size;

    public:
    TV(){size =20;}
    TV(int size){
        this->size=size;
    }
    //멤버 매소드
    int getSize(){
        return size;
    }
};
class WideTV: public TV{
    protected:
bool videoIn;

    public:
    // defalt 생성자 없음
    WideTV(int size,bool videoIn):TV(size){
        this->videoIn=videoIn;
    }
    bool getVideoIn(){return this-> videoIn;}
};

class SmartTV:public WideTV{
    protected:

    public:
    
    string ipAddr;
    SmartTV(string ipAddr,int size):WideTV(size,true){
        this->ipAddr=ipAddr;
    }
    string getIpAddr(){return ipAddr;}
   
};


int main()
{
    SmartTV htv("192.0.0.1",32);
    cout<<"size="<<htv.getSize()<<endl;
    cout<<"videoIn="<<boolalpha<<htv.getVideoIn()<<endl;
    cout<<"IP="<<htv.getIpAddr()<<endl;
    return 0;
}