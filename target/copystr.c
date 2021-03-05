#include <stdio.h>
#include <string.h>

int main(void){
  char src[0x100];
  char dst[0x100];

  printf("input string: ");
  scanf("%s", src);
  strcpy(dst, src);
  printf(dst);

  return 0;
}
