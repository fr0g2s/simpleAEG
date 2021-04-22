sample: sample.c
	gcc -o sample_x86 sample.c -fno-stack-protector -z execstack -no-pie -fno-pic -m32; \
	  gcc -o sample_x64 sample.c -fno-stack-protector -z execstack -no-pie -fno-pic
