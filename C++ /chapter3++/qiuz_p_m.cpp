#include<iostream>
// 4칙연산

class Calculator
{
    private:

    public:
    Calculator(){}

    int plus(int x, int y){
        return x+y;
    }
    int minus(int x, int y){
        return x-y;
    }
   double divide(int x, int y){
        return (double)x/y;
    }
    int multiply(int x,int y){
         return x*y;
    }
};

int main(){

    using namespace std;

    Calculator calculator;

    cout<<"덧셈:"<<calculator.plus(5,7)<<endl;
    cout<<"뻴셈:"<<calculator.minus(5,7)<<endl;
    cout<<"나눗셈:"<<calculator.divide(5,7)<<endl;
    cout<<"뻴셈:"<<calculator.multiply(5,7)<<endl;



    return 0;
}