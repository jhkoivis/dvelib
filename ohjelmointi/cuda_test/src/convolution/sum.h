
#ifndef SUM_H
#define SUM_H

#include <cuda.h>
#include <stdlib.h>
#include <stdio.h>
#include <cutil.h>

#define BLOCK_X 16
#define BLOCK_Y 16

struct CudaMemPointers{
	float	*pSrcImg_host;
	float	*pSrcImg_device;
	float	*pDefImg_host;
	float	*pDefImg_device;
	float	*pSumImg_host;
	float	*pSumImg_device;
	size_t	srcImgPitch;
	size_t	defImgPitch;
	size_t	sumImgPitch;
	int 	xSize;
	int		ySize;
};

int copyHtoD(	struct CudaMemPointers 	*cMem);

int copyDtoH(	struct CudaMemPointers 	*cMem);

/*
 * This calculates a convolution between the two images.
 * It is a kernel function for cuda and does not work properly.
 * Its merely to describe the simplest way of executing cuda-kernel.
 */
__global__ void convolutionKernel(	float *pSrcImg, 	// <-- source image
									size_t srcPitch,	// <-- source image pitch
									float *pDefImg,		// <-- deformed image
									size_t defPitch);	// <-- deformed image pitch

/*
 * Handles all processes from creating data and feeding it to convolution kernel.
 * See source code for details.
 *
 * returns kernel time in ms
 */
float sum(	float	*pRefImage,		// <-- pointer to reference image
			float	*pRefImage,		// <-- pointer to deformed 	image
			float	*pSumImage,		// <-- pointer to sum (result) image
			int		xSize,			// <-- image width
			int		ySize);			// <-- image height


#endif // SUM_H
