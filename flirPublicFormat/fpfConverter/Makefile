

all:
	gcc -Wall -g -c fpfConverterLib.c -o fpfConverterLib.o
	gcc -Wall -g fpfConverter.c fpfConverterLib.o -o fpfConverter

clean:
	rm -f *.o
	rm -f fpfConverter

tests:
	./fpfConverter test/1.fpf test/1.pgm
	display test/1.pgm
