#include <iostream>
#include <cstdint>
#include <cstdlib>

using namespace std;
template  <class T, T default_feed> class LSFR_Galua
{
private:
    T state;
    T feedback;
public:
    LSFR_Galua(T s = 1, T f = default_feed ): state(s), feedback(f) {}
    uint8_t GetNum();
};

typedef LSFR_Galua<uint32_t, 0xE2745687> LSFR_Galua_32;

int main(int argc, char** argv)
{
    if (argc != 2)
    {
        cerr<<"Need parameter - a 32 bit nonzero key in dec, hex or oct format\n";
        return 1;
    }
    uint32_t key;
    char *p;
    key = strtoul(argv[1],&p,0);
    if (*p != '\0' || key == 0)
    {
        cerr<<"Key must be a 32 bit nonzero number in dec, hex or oct format, like c++ constant\n";
        return 2;
    }
    LSFR_Galua_32 rnd(key);
    uint8_t byte;
    while (byte = cin.get(),!cin.eof())
        cout.put(rnd.GetNum() ^ byte);
    cout.flush();
    return 0;
}

template  <class T, T default_feed> uint8_t LSFR_Galua <T, default_feed> ::GetNum()
{
    uint8_t r = 0;
    for (int i = 0; i < 8; i++)
    {
        r <<= 1;
        if (state & 1)
        {
            state = (state >> 1) ^ feedback;
            r |= 1;
        }
        else
        {
            state >>= 1;
        }
    }
    return r;
}