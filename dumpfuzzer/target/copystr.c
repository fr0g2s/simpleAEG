#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(void){
  char src[0x10];
  char dst[0x10];

  printf("input string: ");
  scanf("%s", src);
  strncpy(dst, src, strlen(src));
  write(1, dst, strlen(dst))

  puts("-- END --");

  return 0;
}
