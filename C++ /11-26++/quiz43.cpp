#include <iostream>
#include <cstdlib>
#include <memory>
using namespace std;

class Triangle
{
private:
 
public:
   int width;
    int height;

   double getArea(string width, string height)
    {
        this->width = stoi(width);
        this->height = stoi(height);
       
         
        return this->width*this->height*0.5; 
    }
};

int main()
{
    string width, height;
    getline(cin, width);
    getline(cin, height);
      Triangle tri;
    cout<<tri.getArea(width,height)<<endl;

    return 0;
}
