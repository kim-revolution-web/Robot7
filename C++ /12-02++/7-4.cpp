#include <iostream>
#include <cstdlib>
#include <memory>
using namespace std;

class Power
{
    int kick;
    int punch;

public:
    Power(int kick = 0, int punch = 0)
    {
        this->kick = kick;
        this->punch = punch;
    }
    
    void show()
    {
        cout << "kick:" << kick << ',' << "punch:" << punch << endl;
    }
   
    Power operator-(Power other)
    {
        Power temp;
        temp.kick = this->kick + other.kick;
        temp.punch = this->punch + other.punch;
        return temp;
    }
};

int main()
{
    Power a(3, 5), b(4, 6), c;
    c = a - b;
    a.show();
    b.show();
    c.show();

    return 0;
}