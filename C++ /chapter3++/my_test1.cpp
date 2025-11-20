#include <iostream>
using namespace std;

class Knight 
{
public:
    //1.멤버 변수
    int level;
    string name;
    int hp;
    int mp;
    //2.생성자

Knight(string _name, int _level, int _hp, int _mp)
    :level(_level),name(_name),hp(_hp),mp(_mp) { 
    }


    Knight():Knight("기사",1,100,20){
        
    }
    Knight(string _name, int _level):Knight(_name, _level,100,20) {
       
    }
    
    //3.멤버 함수
    string attack() {
        return "공격하다!!!";
    }
    string attack(string weapon) {
        
        return weapon + "로 공격하다!!!";
    }
    string attack(string weapon, string ora) {
        return ora +" 보호막으로 감싼 후 " + weapon + "로 공격하다!!!";
    }

    string eat() {
        return "먹는다!!!";
    }
};

int main()
{
   //Knight james;
   //Knight james("제임스", 10);
   Knight james("제임스", 20, 90, 10);

   cout << "레벨 : " << james.level << endl; 
   cout << "이름 : " << james.name << endl; 
   cout << "체력 : " << james.hp << endl; 
   cout << "마력 : " << james.mp << endl; 

   cout << james.attack() << endl;
   cout << james.attack("뽕망치") << endl;
   cout << james.attack("뽕망치", "화염") << endl;

   
    return 0;
}