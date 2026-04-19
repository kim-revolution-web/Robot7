#include<iostream>
#include<memory>
#include<cstdlib>
using namespace std;

class Shape{
public:
virtual void draw()
{
    cout<<"도형을 그리다."<<endl;
}


};
class Triangle: public Shape
{
    public:
    void draw() override{
        cout<<"삼각형을 만들다"<<endl;
    }
    
};
class Rectangle: public  Shape{
    public:
    void draw() override{
        cout<<"사각형을 만들다"<<endl;
}
};
class Circle: public  Shape
{
    public:
    void draw() override{
        cout<<"원형을 만들다"<<endl;
    }
    
};


int main(){

Shape* shape[4];//배열선언
shape[0]=new Shape();
shape[1]=new Triangle();
shape[2]=new Rectangle();
shape[3]=new Circle();

for(Shape* s: shape){
    s->draw();
}
//for(auto s: shape)

for(int i=0;i<4;i++){
    delete shape[i];
}

    return 0;
}