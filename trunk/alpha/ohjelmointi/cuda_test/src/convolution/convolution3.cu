
#include <cuda.h>
#include <stdlib.h>
#include <stdio.h>
//#include <cutil.h>

#define BLOCK_X 16
#define BLOCK_Y 16


__global__ void convolutionKernel(	float *pSrcImg, size_t pitch)
{
	int 	x,
			y;
	x = threadIdx.x + blockDim.x * blockIdx.x;
	y = threadIdx.y + blockDim.y * blockIdx.y;
	pSrcImg[x + y*pitch] = 1;
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
			//*pRefImg,
			//*pRefImg_device,
	size_t
			srcImgPitch;
			//refImgPitch;

	int		imDimX = 64,
			imDimY = 64,
			i,
			j,
			testFailed = 0;

	cudaError_t
			cudaError;

	cudaSetDevice(0);

	// memory for the device
	cudaError = cudaMallocPitch(	(void **) &pSrcImg_device,
									&srcImgPitch,
									imDimX*sizeof(float),
									imDimY);
	pce(&cudaError, __LINE__);
	printf("pitch: %d\n", (int)srcImgPitch);

	// memory for the host
	pSrcImg = (float *)calloc(imDimY*imDimX, sizeof(float));
	//cudaError = cudaMallocHost(	(void **)&pSrcImg,
	//							(size_t)imDimX*imDimY*sizeof(float));
	//pce(&cudaError, __LINE__);

	//copy memory from host to device
	cudaError = cudaMemcpy2D(	pSrcImg_device,
								srcImgPitch,
								pSrcImg,
								imDimX*sizeof(float),
								imDimX*sizeof(float),
								imDimY,
								cudaMemcpyHostToDevice);
	pce(&cudaError, __LINE__);

	// create grid (this is c++ ?)
	dim3 block(BLOCK_X,BLOCK_Y);
	dim3 grid(imDimX/BLOCK_X,imDimY/BLOCK_Y);

	convolutionKernel<<< grid, block >>>(	pSrcImg_device,
											srcImgPitch/sizeof(float)); // IMPORTANT SIZEOF
	cudaError = cudaGetLastError();
	pce(&cudaError, __LINE__);
	cudaThreadSynchronize();
	cudaError = cudaGetLastError();
	pce(&cudaError, __LINE__);

	// copy results back
	cudaError = cudaMemcpy2D(	pSrcImg,
								imDimX*sizeof(float),
								pSrcImg_device,
								srcImgPitch,
								imDimX*sizeof(float),
								imDimY,
								cudaMemcpyDeviceToHost);
	pce(&cudaError, __LINE__);
	for (i = 0; i < imDimX; i++)
	{
		for (j=0; j < imDimY; j++)
		{
			if ((int)pSrcImg[i+j*imDimY] != 1)
				{
					//printf("%d, %d: %f\n", i,j,pSrcImg[i+j*imDimY]);
					testFailed = 1;
				}
			else
			{
				//printf("%d, %d: %f\n", i,j,pSrcImg[i+j*imDimY]);
			}
		}
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
