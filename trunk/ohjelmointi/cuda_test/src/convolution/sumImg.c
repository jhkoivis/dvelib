
#include "sumImg.h"
#include "sum.h"

int parseInputs(int argc, char **argv, struct Storage *s)
{
	if (argc != 6) return 1;

	s->params.pRefImFn = argv[1];
	s->params.pDefImFn = argv[2];
	s->params.pSumImFn = argv[3];
	if (sscanf(argv[4], "%d", &(s->params.xSize)) != 1)
		return 2;
	if (sscanf(argv[5], "%d", &(s->params.ySize)) != 1)
		return 3;

	return 0;
}

void pe(int line)
{
	printf("Error in line: %d\n", line);
}

int reserveMemoryForImages(struct Storage *s)
{
	int x,y;

	x = s->params.xSize;
	y = s->params.ySize;
	s->mem.pRefImage = (float *)malloc(x*y*sizeof(float));
	if (s->mem.pRefImage == NULL) return 1;
	s->mem.pDefImage = (float *)malloc(x*y*sizeof(float));
	if (s->mem.pDefImage == NULL) return 2;
	s->mem.pSumImage = (float *)malloc(x*y*sizeof(float));
	if (s->mem.pDefImage == NULL) return 3;

	return 0;
}

int loadSingleImage(char *pImFn, float *pIm, int xSize, int ySize)
{
	FILE 	*pImage;
	int 	i = 0,
			j = 0,
			k = 0;
	char	line[1000];
	float	data;

	pImage = fopen(pImFn, "r");

	line[k] = getc(pImage);
	while (!feof(pImage))
	{
		if ((line[k] == ',') || (line[k] == '\n'))
		{
			line[k] = '\0';
			sscanf(line, "%f", &data);
			pIm[i + j*xSize] = data;
			k = 0;
			if (i < (xSize-1)){
				i++;
			}
			else{
				i = 0;
				j++;
			}
		}
		else{
			k++;
		}
		line[k] = getc(pImage);
	}
	// check if everything is scanned (missing '\n' at the last line)
	if (k != 0)
	{
		//line[k] = '\0';
		sscanf(line, "%f", &data);
		pIm[i + j*xSize] = data;
	}

	return 0;
}

int loadImages(struct Storage *s)
{
	int rVal = 0;

	rVal = loadSingleImage(	s->params.pRefImFn,
							s->mem.pRefImage,
							s->params.xSize,
							s->params.ySize);
	if (rVal) return rVal;

	rVal = loadSingleImage(	s->params.pDefImFn,
							s->mem.pDefImage,
							s->params.xSize,
							s->params.ySize);
	if (rVal) return rVal;

	return 0;
}

int saveSingleImage(char *pImFn, float *pIm, int xSize, int ySize)
{
	FILE	*image;
	int		i,
			j;
	image = fopen(pImFn, "w");
	for (j = 0; j < ySize; j++)
	{
		for (i = 0; i < xSize; i++)
		{
			fprintf(image, "%.7f", pIm[i + j*xSize]);
			if (i == xSize-1){
				fprintf(image, "\n");
			}
			else{
				fprintf(image, " ");
			}
		}
	}
	return 0;
}

int main(int argc, char **argv) {

	struct Storage	s;
	float kernelTimeInMs;

	// parse inputs
	if (parseInputs(argc, argv, &s)) pe(__LINE__);
	/*
	printf(	"%s\n%s\n%s\n%d\n%d\n",
			s.params.pRefImFn,
			s.params.pDefImFn,
			s.params.pSumImFn,
			s.params.xSize,
			s.params.ySize);
	fflush(stdout);
	*/

	// reserve memory
	if (reserveMemoryForImages(&s)) pe(__LINE__);

	// load image data
	if (loadImages(&s)) pe(__LINE__);

	kernelTimeInMs = sum(	s.mem.pRefImage,
							s.mem.pDefImage,
							s.mem.pSumImage,
							s.params.xSize,
							s.params.ySize);
	printf("Kernel time: %f (ms)", kernelTimeInMs);

	// save image data
	if (saveSingleImage(s.params.pSumImFn,
						s.mem.pSumImage,
						s.params.xSize,
						s.params.ySize))
		pe(__LINE__);

	return 0;
}
