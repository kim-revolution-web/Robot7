#include <iostream>

class Rectangle
{
public:

    int width;
    int height;

    
    int getArea()
    {
        return width*height;};
    };

int main()
{
    using namespace std;
   Rectangle rect;
   rect.width =3;
   rect.height =5;
   cout<< "사각형의 면적은"<<rect.getArea()<<endl;

    return 0;
}