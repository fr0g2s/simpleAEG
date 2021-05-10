sample: sample.c
	gcc -o sample_x86 sample.c -fno-stack-protector -z execstack -no-pie -fno-pic -m32 -z relro -z now;\
	  gcc -o sample_x64 sample.c -fno-stack-protector -z execstack -no-pie -fno-pic

sample2: sample2.c
	gcc -o sample2_x86 sample2.c -fno-stack-protector -z execstack -no-pie -fno-pic -m32 ;
