
#include "convolution.h"

__global__ void convolutionKernel(	float *pSrcImg,
									size_t srcPitch,
									float *pDefImg,
									size_t defPitch)
{
	int 	x,
			y;
	x = threadIdx.x + blockDim.x * blockIdx.x;
	y = threadIdx.y + blockDim.y * blockIdx.y;
	pDefImg[x + y*defPitch] = pSrcImg[x + y*srcPitch];
}

void pce(	cudaError_t *pCudaError,
			int lineNumber)
{
	if (*pCudaError) printf( 	"cudaError at line %d:\n  %s\n",
								lineNumber,
								cudaGetErrorString(*pCudaError));
}

int main(void) {

	float 	*pSrcImg,
			*pSrcImg_device,
			*pDefImg,
			*pDefImg_device,
			testValue;
	size_t
			srcImgPitch,
			defImgPitch;

	int		imDimX = 2048,
			imDimY = 2048,
			i,
			j,
			testFailed = 0;

	cudaError_t
			cudaError;

	unsigned int timer = 0;
	float compute_time;

	cudaSetDevice(0);

	// memory for the device
	cudaError = cudaMallocPitch(	(void **) &pSrcImg_device,
									&srcImgPitch,
									imDimX*sizeof(float),
									imDimY);
	pce(&cudaError, __LINE__);
	cudaError = cudaMemset2D (	pSrcImg_device,
								srcImgPitch,
								0,
								imDimX*sizeof(float),
								imDimY);
	pce(&cudaError, __LINE__);
	cudaError = cudaMallocPitch(	(void **) &pDefImg_device,
									&defImgPitch,
									imDimX*sizeof(float),
									imDimY);
	pce(&cudaError, __LINE__);
	cudaError = cudaMemset2D (	pDefImg_device,
								defImgPitch,
								0,
								imDimX*sizeof(float),
								imDimY);
	pce(&cudaError, __LINE__);


	// memory for the host
	pSrcImg = (float *)calloc(imDimY*imDimX, sizeof(float));
	pDefImg = (float *)calloc(imDimY*imDimX, sizeof(float));

	for (i = 0; i < imDimX; i++)
	{
		for (j = 0; j < imDimY; j++)
		{
			pSrcImg[i + j*imDimX] = (RANDNUM);
		}
	}

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
	cudaError = cudaMemcpy2D(	pDefImg_device,
								defImgPitch,
								pDefImg,
								imDimX*sizeof(float),
								imDimX*sizeof(float),
								imDimY,
								cudaMemcpyHostToDevice);
	pce(&cudaError, __LINE__);

	// create grid (this is c++ ?)
	dim3 block(BLOCK_X,BLOCK_Y);
	dim3 grid(imDimX/BLOCK_X,imDimY/BLOCK_Y);


	CUT_SAFE_CALL(cutCreateTimer(&timer));
	CUT_SAFE_CALL(cutStartTimer(timer));
	convolutionKernel<<< grid, block >>>(	pSrcImg_device,
											srcImgPitch/sizeof(float),
											pDefImg_device,
											defImgPitch/sizeof(float)); // IMPORTANT SIZEOF
	cudaError = cudaGetLastError();
	pce(&cudaError, __LINE__);
	cudaThreadSynchronize();
	cudaError = cudaGetLastError();
	pce(&cudaError, __LINE__);

	CUT_SAFE_CALL(cutStopTimer(timer));
	compute_time = cutGetTimerValue(timer);
	cutDeleteTimer(timer);
	printf("kernel execution time : %f (ms)\n", compute_time);




	// copy results back
	cudaError = cudaMemcpy2D(	pSrcImg,
								imDimX*sizeof(float),
								pSrcImg_device,
								srcImgPitch,
								imDimX*sizeof(float),
								imDimY,
								cudaMemcpyDeviceToHost);
	pce(&cudaError, __LINE__);
	cudaError = cudaMemcpy2D(	pDefImg,
								imDimX*sizeof(float),
								pDefImg_device,
								defImgPitch,
								imDimX*sizeof(float),
								imDimY,
								cudaMemcpyDeviceToHost);
	pce(&cudaError, __LINE__);
	for (i = 0; i < imDimX; i++)
	{
		for (j=0; j < imDimY; j++)
		{
			testValue = (pSrcImg[i+j*imDimX] - (RANDNUM))* (pSrcImg[i+j*imDimX] - (RANDNUM));
			if (testValue > 0.001 )
				{
					//printf("%d, %d: %f", i,j,pSrcImg[i+j*imDimX]);
					//printf(" %f\n", (RANDNUM));
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
	cudaError = cudaFree(pSrcImg_device);
	pce(&cudaError, __LINE__);
	cudaError = cudaFree(pDefImg_device);
	pce(&cudaError, __LINE__);
	//cudaError = cudaFreeHost(	(void **)&pSrcImg);
	//pce(&cudaError, __LINE__);

	return cudaError;

}
