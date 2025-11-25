#include <iostream>


using namespace std;

class Horse{
    public:
    void run(){
        cout <<"달리다"<<endl;
    }

};

class Bird{
    public:
    void fly(){
        cout <<"날다"<<endl;
    }

};

class A{
    public:
   
};

class Unicorn:public Horse,public Bird{

    

};


int main()
{
    Unicorn mary;
    mary.run();
    mary.fly();
    


    return 0;
}