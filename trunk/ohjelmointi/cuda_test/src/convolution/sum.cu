
#include "sum.h"

__global__ void convolutionKernel(	float *pSrcImg,
									size_t srcPitch,
									float *pDefImg,
									size_t defPitch,
									float *pSumImg,
									size_t sumPitch)
{
	int 	x,
			y;
	x = threadIdx.x + blockDim.x * blockIdx.x;
	y = threadIdx.y + blockDim.y * blockIdx.y;

	pSumImg[x + y*sumPitch] = 	pDefImg[x + y*defPitch] +
								pSrcImg[x + y*srcPitch];
}

void pce(	cudaError_t *pCudaError,
			int lineNumber)
{
	if (*pCudaError) printf( 	"cudaError at line %d:\n  %s\n",
								lineNumber,
								cudaGetErrorString(*pCudaError));
}

int copyHtoD(struct	CudaMemPointers	*cMem)
{
	cudaError_t
			cudaError;

	// memory for the device
	cudaError = cudaMallocPitch((void **) &(cMem->pSrcImg_device),
								&(cMem->srcImgPitch),
								cMem->xSize*sizeof(float),
								cMem->ySize);
	pce(&cudaError, __LINE__);
	cudaError = cudaMemset2D (	cMem->pSrcImg_device,
								cMem->srcImgPitch,
								0,
								cMem->xSize*sizeof(float),
								cMem->ySize);
	pce(&cudaError, __LINE__);

	cudaError = cudaMallocPitch((void **) &(cMem->pDefImg_device),
								&(cMem->defImgPitch),
								cMem->xSize*sizeof(float),
								cMem->ySize);
	pce(&cudaError, __LINE__);
	cudaError = cudaMemset2D (	cMem->pDefImg_device,
								cMem->defImgPitch,
								0,
								cMem->xSize*sizeof(float),
								cMem->ySize);
	pce(&cudaError, __LINE__);

	cudaError = cudaMallocPitch((void **) &(cMem->pSumImg_device),
								&(cMem->sumImgPitch),
								cMem->xSize*sizeof(float),
								cMem->ySize);
	pce(&cudaError, __LINE__);
	cudaError = cudaMemset2D (	cMem->pSumImg_device,
								cMem->sumImgPitch,
								0,
								cMem->xSize*sizeof(float),
								cMem->ySize);
	pce(&cudaError, __LINE__);

	//copy memory from host to device
	cudaError = cudaMemcpy2D(	cMem->pSrcImg_device,
								cMem->srcImgPitch,
								cMem->pSrcImg_host,
								cMem->xSize*sizeof(float),
								cMem->xSize*sizeof(float),
								cMem->ySize,
								cudaMemcpyHostToDevice);
	pce(&cudaError, __LINE__);

	cudaError = cudaMemcpy2D(	cMem->pDefImg_device,
								cMem->defImgPitch,
								cMem->pDefImg_host,
								cMem->xSize*sizeof(float),
								cMem->xSize*sizeof(float),
								cMem->ySize,
								cudaMemcpyHostToDevice);
	pce(&cudaError, __LINE__);

	cudaError = cudaMemcpy2D(	cMem->pSumImg_device,
								cMem->sumImgPitch,
								cMem->pSumImg_host,
								cMem->xSize*sizeof(float),
								cMem->xSize*sizeof(float),
								cMem->ySize,
								cudaMemcpyHostToDevice);
	pce(&cudaError, __LINE__);

	return 0;
}

int copyDtoH(	struct CudaMemPointers 	*cMem)
{
	cudaError_t
			cudaError;

	cudaError = cudaMemcpy2D(	cMem->pSrcImg_host,
								cMem->xSize*sizeof(float),
								cMem->pSrcImg_device,
								cMem->srcImgPitch,
								cMem->xSize*sizeof(float),
								cMem->ySize,
								cudaMemcpyDeviceToHost);
	pce(&cudaError, __LINE__);

	cudaError = cudaMemcpy2D(	cMem->pDefImg_host,
								cMem->xSize*sizeof(float),
								cMem->pDefImg_device,
								cMem->defImgPitch,
								cMem->xSize*sizeof(float),
								cMem->ySize,
								cudaMemcpyDeviceToHost);
	pce(&cudaError, __LINE__);

	cudaError = cudaMemcpy2D(	cMem->pSumImg_host,
								cMem->xSize*sizeof(float),
								cMem->pSumImg_device,
								cMem->defImgPitch,
								cMem->xSize*sizeof(float),
								cMem->ySize,
								cudaMemcpyDeviceToHost);
	pce(&cudaError, __LINE__);

	return 0;
}

float sum(float *pSrcImg,
		float *pDefImg,
		float *pSumImg,
		int xSize,
		int ySize) {

	CudaMemPointers	cMem;

	//int		i,
	//		j,
	//		testFailed = 0;

	cudaError_t
			cudaError;

	unsigned int timer = 0;
	float compute_time;

	/*
	for (i = 0; i < imDimX; i++)
	{
		for (j=0; j < imDimY; j++)
		{
			printf(	"%d, %d: %f %f %f\n", i,j,
				pSrcImg[i+j*imDimX],
				pDefImg[i+j*imDimX],
				pSumImg[i+j*imDimX]);
		}
	}
	*/

	cMem.pSrcImg_host = pSrcImg;
	cMem.pDefImg_host = pDefImg;
	cMem.pSumImg_host = pSumImg;
	cMem.xSize = xSize;
	cMem.ySize = ySize;

	cudaSetDevice(0);

	// copy data from host to device
	// fixme: this also reserves memory -> make separate function
	copyHtoD(&cMem);

	// create grid (this is c++ ?)
	dim3 block(BLOCK_X,BLOCK_Y);
	dim3 grid(cMem.xSize/BLOCK_X,cMem.ySize/BLOCK_Y);


	CUT_SAFE_CALL(cutCreateTimer(&timer));
	CUT_SAFE_CALL(cutStartTimer(timer));
	convolutionKernel<<< grid, block >>>(	cMem.pSrcImg_device,
											cMem.srcImgPitch/sizeof(float),
											cMem.pDefImg_device,
											cMem.defImgPitch/sizeof(float),
											cMem.pSumImg_device,
											cMem.sumImgPitch/sizeof(float)); // IMPORTANT SIZEOF
	cudaError = cudaGetLastError();
	pce(&cudaError, __LINE__);
	cudaThreadSynchronize();
	cudaError = cudaGetLastError();
	pce(&cudaError, __LINE__);

	CUT_SAFE_CALL(cutStopTimer(timer));
	compute_time = cutGetTimerValue(timer);
	cutDeleteTimer(timer);
	//printf("kernel execution time : %f (ms)\n", compute_time);

	// copy results back
	copyDtoH(&cMem);

	/*
	for (i = 0; i < imDimX; i++)
	{
		for (j=0; j < imDimY; j++)
		{
			testValue = pSrcImg[i + j*imDimX] + pDefImg[i + j*imDimX];
			testValue = testValue - pSumImg[i + j*imDimX];
			testValue = testValue * testValue;
			if (testValue > 0.001 )
				{
					printf("%d, %d: %f", i,j,pSrcImg[i+j*imDimX]);
					//printf(" %f\n", (RANDNUM));
					testFailed = 1;
				}
			else
			{
				printf(	"%d, %d: %f %f %f\n", i,j,
						pSrcImg[i+j*imDimX],
						pDefImg[i+j*imDimX],
						pSumImg[i+j*imDimX]);

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
	*/

	// free data
	//cudaError = cudaFree(pSrcImg_device);
	//pce(&cudaError, __LINE__);
	//cudaError = cudaFree(pDefImg_device);
	//pce(&cudaError, __LINE__);
	//cudaError = cudaFreeHost(	(void **)&pSrcImg);
	//pce(&cudaError, __LINE__);

	return compute_time;

}
