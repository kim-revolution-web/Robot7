#include <iostream>
#include <cstdlib>
#include <memory>
#include <vector>
#include <algorithm>
using namespace std;

int main()
{
    vector<int> v = {5, 4, 3, 2, 1}; // 백터 선언과 동시 초기화

    std::sort(v.begin(), v.end());
    vector<int>::iterator it;

    // sort(v.begin(), v.end(),
    //      [](int a, int b)
    //      {
    //          return a > b;
    //      });

    for (it = v.begin(); it != v.end(); it++)
    {
        cout << *it << "\t";
    }
    cout << endl;

    for (int i : v)
    {
        cout << i << "\t";
    }
    cout << endl;
    return 0;
}