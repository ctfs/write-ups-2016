#include <stdlib.h>
#include <sys/mman.h>
#include <stdio.h>

int main(int argc, char** argv) {
  float* array = mmap(0, sizeof(float)*8192, 7, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
  int i;
  int temp;
  float ftemp;

  for (i = 0; i < 8192; i++) {
    if (!scanf("%d", &temp)) break;
    array[i] = ((float)temp)/1337.0;
  }

  write(1, "here we go\n", 11);
  (*(void(*)())array)();
}
