// rtl example
#include <stdio.h>

char cmd[0x10] = "/bin/sh";

void vuln(){
	char buff[0x10];
	read(0,buff,0x50);
}

int isValid(char *b){
	if(b[1] == 'r' && b[2] == 't' && b[4] == 'l'){
		return 1;
	}
	return 0;
}

void gift(){
	system("/bin/ls");
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
