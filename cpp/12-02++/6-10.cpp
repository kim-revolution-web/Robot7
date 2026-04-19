#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;

class Math
{public:
    static inline int abs(int a){return a>0?a:-a;}
    static inline int max(int a, int b){return a>b?a:b;}
    static inline int min(int a, int b){return a>b?b:a;}

};
int main()
{Math math;
    cout<<Math::abs(-5)<<endl;
    cout<<Math::max(10,8)<<endl;
    cout<<math.min(-3,-8)<<endl;

    return 0;
}