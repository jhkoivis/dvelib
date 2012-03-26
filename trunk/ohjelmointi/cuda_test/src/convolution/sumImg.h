
#ifndef SUMIMG_H
#define SUMIMG_H

#include <stdio.h>
#include <stdlib.h>
#include <sum.h>

#define MAXLINELENGTH 1000000

/*
 * store input parameters here
 */
struct InputParameters{
	char	*pRefImFn;		// <-- pointer to reference image filename
	char	*pDefImFn;		// <-- pointer to deformed  image filename
	char	*pSumImFn;		// <-- pointer to sum 		image filename
	int		xSize;			// <-- xSize of the images
	int 	ySize;			// <-- ySize of the images
};

/*
 *	Storage for host memory pointers.
 */
struct ImageMemoryPointers{
	float 	*pRefImage;		// <-- pointer to reference image memory
	float 	*pDefImage;		// <-- pointer to reference image memory
	float 	*pSumImage;		// <-- pointer to reference image memory
};

/*
 * All data struct
 */
struct Storage{
	struct InputParameters			params;	// <-- parameters data (pRefImFn, pDefImFn, pSumImFn, xSize, ySize)
	struct ImageMemoryPointers		mem;	// <-- memory data (pRefImage, pDefImage, pSumImage)
};

/*
 * Reserves memory for images.
 *
 * return values:
 * 		0		Success
 * 		1		Cannot reserve memory for reference image
 * 		2		Cannot reserve memory for deformed image
 * 		3		Cannot reserve memory for sum image
 */
int reserveMemoryForImages(
		struct Storage 	*s); 	// <-- pointer for information struct

/*
 * Print error
 */
void pe(
		int line);		// <-- line number of the error

/*
 *	Parse inputs to parameters and check the validity.
 *
 *	return values:
 *		0		Success
 *		1		Wrong number of arguments
 *		2		Input argument 4 is not integer (xSize).
 *		2		Input argument 5 is not integer (ySize).
 */
int parseInputs(
		int 			argc,	// <-- argument count
		char 			**argv,	// <-- argument array
		struct Storage 	*s);	// <-- pointer to all information

/*
 * Loads data information.
 */
int loadImages(
		struct Storage	*s);	// <-- Data storage that includes image information

/*
 * Loads single image to memory.
 */
int loadSingleImage(
		char 	*pImFn,	// <-- Image file name
		float 	*pIm,	// <-- pointer to memory
		int 	xSize,	// <-- image width
		int 	ySize);	// <-- image height

/*
 * Save single image to disk.
 */
int saveSingleImage(
		char 	*pImFn,	// <-- Image file name
		float 	*pIm,	// <-- pointer to memory
		int 	xSize,	// <-- image width
		int 	ySize);	// <-- image height

#endif // SUMIMG_H



