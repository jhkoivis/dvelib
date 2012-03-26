
#include <stdio.h>
#include <cuda.h>

#define	SIM_THREADS		10		// how many simultaneus threads
#define N	20 					// number of variables in a vector


// this function returns a result
__global__ void dummyFunct(float *pResult)
{
	int i;
	float previous = 0.0;
	pResult[0] = 0.0;
	// this loop will do sequences:
	//	i = 0, 10, 20, ...
	//  i = 1, 11, 21, ...
	//  i = 2, 12, 22, ...
	//  ...
	//  i = 9, 19, 29, ...
	//
	// assuming SIM_THREADS = 10

	for (	i = threadIdx.x;	// start from i = thread ID
			i < N; 				// stop if all i's are done
			i += SIM_THREADS)	// skip number of threads
		pResult[i] = previous + i;
		previous = pResult[i];
}

int main(void)
{
	float *pHostResult;
	float *pCudaResult = 0;
	int i;

	// reserve memory in host system
	pHostResult = (float *) malloc(N*sizeof(pHostResult[0]));

	// reserve memory in cuda
	cudaMalloc((void **) &pCudaResult, N*sizeof(pCudaResult[0]));

	dummyFunct<<<1,SIM_THREADS>>>(pCudaResult);

	// copy result from cuda to host
	cudaMemcpy(	pHostResult, 				// destination
				pCudaResult, 				// source
				N*sizeof(pCudaResult[0]),	// amount to copy
				cudaMemcpyDeviceToHost);	// type: device -> host

	for (i = 0; i < N; i++)
		printf("%f\n", pHostResult[i]);
}


