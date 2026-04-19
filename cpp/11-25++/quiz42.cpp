#include <iostream>
#include <cstdlib>
#include <memory>
using namespace std;

class wizerd
{
public:
    void maic()
    {
        cout << "마법" << endl;
    }
};

class waterwizerd :virtual public wizerd
{
public:
    void water()
    {
        cout << "물" << endl;
    }
};
class flywizerd :virtual public wizerd
{
public:
   void fly()
    {
        cout << "공중" << endl;
    }
};

class treewizerd : public waterwizerd, public flywizerd
{
public:
    void tree()
    {
        cout << "나무" << endl;
    }
};

int main()
{
    treewizerd tw;
    tw.maic();
    tw.fly();
    tw.fly();
    tw.tree();
    return 0;
}