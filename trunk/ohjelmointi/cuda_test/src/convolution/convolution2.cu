
#include <cuda.h>
#include <stdlib.h>
#include <stdio.h>
//#include <cutil.h>

#define BLOCK_X 16
#define BLOCK_Y 16


__global__ void convolutionKernel(	float *pSrcImg)
{
	int 	x,
			y;
	x = threadIdx.x + blockDim.x * blockIdx.x;
	y = threadIdx.y + blockDim.y * blockIdx.y;
	pSrcImg[x + y*blockDim.x] = 1;
}

void pce(	cudaError_t *pCudaError,
			int lineNumber)
{
	if (*pCudaError) printf( 	"cudaError at line %d:\n  %s\n",
								lineNumber,
								cudaGetErrorString(*pCudaError));
}

int main(int argc, char **argv) {

	float 	*pSrcImg,
			*pSrcImg_device;
	//size_t
	//		srcImgPitch;

			//*pRefImg,
			//*pRefImg_device,
			//refImgPitch;

	int		imDimX = 16,
			imDimY = 16,
			i,
			testFailed = 0;

	cudaError_t
			cudaError;

	cudaSetDevice(0);

	// memory for the device
	cudaError = cudaMalloc(	(void **) &pSrcImg_device,
							imDimY*imDimX*sizeof(float));
	pce(&cudaError, __LINE__);

	// memory for the host
	pSrcImg = (float *)calloc(imDimY*imDimX, sizeof(float));
	//cudaError = cudaMallocHost(	(void **)&pSrcImg,
	//							(size_t)imDimX*imDimY*sizeof(float));
	//pce(&cudaError, __LINE__);

	//copy memory from host to device
	cudaError = cudaMemcpy(pSrcImg_device,
							pSrcImg,
							imDimY*imDimX*sizeof(float),
							cudaMemcpyHostToDevice);
	pce(&cudaError, __LINE__);

	// create grid (this is c++ ?)
	dim3 block(	BLOCK_X,1);
	dim3 grid(imDimX*imDimY/BLOCK_X,1);

	convolutionKernel<<< grid, block >>>(pSrcImg_device);
	cudaError = cudaGetLastError();
	pce(&cudaError, __LINE__);
	cudaThreadSynchronize();
	cudaError = cudaGetLastError();
	pce(&cudaError, __LINE__);

	// copy results back
	cudaError = cudaMemcpy(	pSrcImg,
							pSrcImg_device,
							imDimY*imDimX*sizeof(float),
							cudaMemcpyDeviceToHost);
	pce(&cudaError, __LINE__);
	for (i = 0; i < imDimX*imDimY; i++)
	{
		if ((int)pSrcImg[i] != 1) testFailed = 1;
	}
	if (testFailed != 0)
	{
		printf("Test failed\n");
	}
	else
	{
		printf("Test passed\n");
	}

	// free data
	//cudaError = cudaFree(		(void **)&pSrcImg_device);
	//pce(&cudaError, __LINE__);
	//cudaError = cudaFreeHost(	(void **)&pSrcImg);
	//pce(&cudaError, __LINE__);

	return cudaError;

}
