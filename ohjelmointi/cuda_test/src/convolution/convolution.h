
#ifndef CONVOLUTION_H
#define CONVOLUTION_H

#include <cuda.h>
#include <stdlib.h>
#include <stdio.h>
#include <cutil.h>

#define BLOCK_X 32
#define BLOCK_Y 16

#define RANDNUM (i*3.1 - 4.6*j) / 8.0

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
 */
int main(void);


#endif // CONVOLUTION_H
