#include<iostream>
using namespace std;


class Dog{
private:
int size;
string eat;
string name;
string color;

public:
Dog():size(130),eat("고기"),name("gordi"),color("blue"){}
Dog(int _size,string _eat,string _name,string _color):
size(_size),eat(_eat),name(_name),color(_color){}

void setSize(int _size){
    size=_size;
}
void setEat(string _eat){
    eat=_eat;
}

void setName(string _name){
    name=_name;
}
void setColor(string&_color){
    color=_color;
}

int getSize(){
   return size;
}
string getEat(){
    return eat;
}

string  getName(){
   return name;
}
string  getColor(){
    return color;
}

};

int main(){
    Dog mungmung;
    cout << "mungmung: "
         << mungmung.getSize() << " "
         << mungmung.getEat() << " "
         << mungmung.getName() << " "
         << mungmung.getColor() << endl;
    Dog bow(170,"사료","바우","회색");
    cout << bow.getColor() << endl;
    Dog *wal = new Dog;
    wal ->setEat("생선");
    cout << wal->getEat()<<endl;




    return 0;
}
