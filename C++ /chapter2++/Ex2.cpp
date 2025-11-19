#include <iostream>

int main()
{
    double width;
    int a, b;

    //std::cin >> a >> b >> std::endl;//이건 에러 
    std::cin >> a >> b;
    width = a * b * 0.5;
    std::cout << width << std::endl;


    return 0;
}
