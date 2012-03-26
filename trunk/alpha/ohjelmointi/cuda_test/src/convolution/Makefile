
oCompFlags=-I /Developer/GPU_Computing/C/common/inc/
linkFlags=/Developer/GPU_Computing/C/lib/libcutil_i386.a

all:
	make clean
	#make tests
	make sumImg

tests:
	/opt/local/bin/python2.6 test_convolution.py

sumImg:
	cp sumImg.c sumImg.cu
	nvcc -g -G ${oCompFlags} -c sum.cu -o sum.o
	nvcc -g -G ${oCompFlags} -c sumImg.cu -o sumImg.o
	nvcc -g -G ${linkFlags} sum.o sumImg.o -o sumImg
	#gcc -g -Wall sumImg.c -o sumImg

convolution:
	nvcc ${flags} convolution.cu -o convolution

clean:
	rm -f /tmp/refImg.*
	rm -f /tmp/defImg.*
	rm -f /tmp/sumImg.*
	rm -f convolution
	rm -f sumImg
	rm -f *.o	
