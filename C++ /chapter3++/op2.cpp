#include <iostream>
#include <memory>
#include <cstdlib>
using namespace std;

class game
{
public:
    virtual void rpg()
    {

        cout << "rpg 최고" << endl;
    }
};

class srpg : public game
{

public:
    void rpg() override
    {
        cout << "srpg 최고" << endl;
    }
};

class arpg : public game
{

public:
    void rpg() override
    {
        cout << "arpg 최고" << endl;
    }
};

class mmorpg : public game
{

public:
    void rpg() override
    {
        cout << "mmorpg 최고" << endl;
    }
};

int main()
{
    game *g[4];
   g[0] = new game;
    g[1] = new srpg;
    g[2] = new arpg;
    g[3] = new mmorpg;
    for(int i =0;i<4;i++){
        g[i]->rpg();
    }

    for(int i =0;i<4;i++){
        delete g[i];
    }

    return 0;
}