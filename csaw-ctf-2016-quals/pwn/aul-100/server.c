
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

#define BUFSIZE 1024

// LUA Funcs

int lua_log(lua_State* L) {
    const char* param1 = luaL_checkstring(L, 1);
    
    fprintf(stderr, "%s\n", param1);
    
    return 0;
}

int lua_readline(lua_State* L) {
  char buf[BUFSIZE];

  memset(buf, '\0', BUFSIZE);

  int i = 0;
  while(read(0, &buf[i], 1) > 0 && buf[i] != '\n' && i < BUFSIZE - 1) {
    ++i;
  }

  buf[i] = '\0';

  lua_pushstring(L, buf);

  return 1;
}

int lua_csaw_writeline(lua_State* L) {
  const char* param1 = luaL_checkstring(L, 1);
  const int size = strlen(param1);

  write(1, param1, size);

  return 0;
}

int lua_writeraw(lua_State* L) {
  const char* param1 = luaL_checkstring(L, 1);
  const size_t size = luaL_checkinteger(L, 2);

  write(1, param1, size);

  return 0;
}

void start_lua(void* _sock) {
  lua_State *L = luaL_newstate();

  luaL_openlibs(L);

  const luaL_Reg log_lib[] = {
      {"log",       &lua_log},
      {"readline",  &lua_readline},
      {"writeline", &lua_csaw_writeline},
      {"writeraw",  &lua_writeraw},
      {NULL,        NULL}
  };

  lua_pushglobaltable(L);
  luaL_setfuncs(L, log_lib, 0);

  int fl = luaL_dostring(L, "dofile('./server.luac');");
      
  if(fl != 0){
      fprintf(stderr, "lua Error: %s\n", lua_tostring(L, -1));
      lua_pop(L, 1);
  }
  
  lua_close(L);
}

/*
 * error - wrapper for perror
 */
void error(char *msg) {
  perror(msg);
  exit(1);
}

int main(int argc, char **argv) {
  start_lua(NULL);

  return 0;
}