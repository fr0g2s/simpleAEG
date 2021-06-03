// rop example
#include <stdio.h>

void vuln(){
	char buff[0x10];
	read(0,buff,0x50);
}

int isValid(char *b){
	if(b[1] == 'r' && b[2] == 'o' && b[4] == 'p'){
		return 1;
	}
	return 0;
}

int main(void){
	char buff[0x10];
	read(0, buff, 0x10);
	if(isValid(buff)){
		puts("nice !");
		vuln();
	}
	else{
		puts("nah..");
	}
	return 0;
}
