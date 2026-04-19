#include <iostream>
#include <cstdlib>
#include<memory>
#include<random>
#include<numeric>
#include<algorithm>

using namespace std;

int main()
{
    //1.난수 발생
    random_device rd;//랜덤 디바이스 객체
    mt19937 gen(rd());//랜덤 객체를ㄹ 매개변수로 생성하며 전달

    //2.1~45 숫자 발생
    vector<int> pool(45);
    iota(pool.begin(),pool.end(),1);//순서대로 1 2 3 4 5 6.. 45

    //3. 섞어주기
    shuffle(pool.begin(),pool.end(),gen);

    //4. 로또번호, 보너스번호(정렬하기전에 추출)
    vector<int> lotto(pool.begin(),pool.begin()+6);
    int bonus = pool[6];//7개 숫자중 마지막을 보너스 번호

    //5.정렬
    sort(lotto.begin(),lotto.end());

    //6.출력
    cout <<"로또 번호:";
    for(int n:lotto){
        cout<<n<<" ";
    }
cout<<"\n보너스 번호:"<<bonus<<endl;

    
    
    return 0;
}