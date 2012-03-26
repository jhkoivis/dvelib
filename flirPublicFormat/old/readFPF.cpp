
#include "Fpfimg.h"
#include <stdio.h>

int readImageData(FILE *inFile)
{
	int i;

	for (i = 0; i < sizeof(FPF_IMAGE_DATA_T); i++)
	{
		printf("%c", getc(inFile));
	}

	return 0;
}

int readHeader(FILE *inFile)
{
	for (int i = 0; i < sizeof(FPFHEADER_T); i++) getc(inFile);

	return 0;
}

int readData(FILE *inFile)
{
	float data;

	while (!feof(inFile))
	{
	    fread(&data, sizeof(data), 1, inFile);
		printf("%f\n", data);
	}
	return 0;
}

int main(void)
{
	FILE *pFpfFile;

	pFpfFile = fopen("test_03-061.FPF","r");

	readHeader(pFpfFile);
	readData(pFpfFile);


	return 0;
}
