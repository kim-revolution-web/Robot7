#include <iostream>
#include <cstdlib>
#include<memory>
using namespace std;
class Tiger{

};
int main()
{
    //shared_ptr
  unique_ptr<Tiger> horang= make_unique<Tiger>();
  unique_ptr<Tiger> hodori;
  
  hodori = std::move(horang);
    return 0;
}