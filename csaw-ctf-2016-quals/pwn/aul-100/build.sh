# really need to do this only once
cd ./lua-5.3.3
make linux
make local
cd ../

# everytime the challenge changes
gcc -I./lua-5.3.3/install/include/ -L./lua-5.3.3/install/lib/ -o scripty server.c -llua -lm -ldl

./lua-5.3.3/install/bin/luac -s -o server.luac server.lua
