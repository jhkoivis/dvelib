
#include <stdio.h>
#include <cuda.h>

#define	SIM_THREADS		10		// how many simultaneus threads
#define N	20 					// number of variables in a vector


// this function returns a result
__global__ void cudaFunct(float *pArgument, float *pResult)
{
	int i;
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
		pResult[i] = pArgument[i] -pArgument[i-1];
}

int main(void)
{
	float *pHostArgument;
	float *pCudaArgument = 0;
	float *pHostResult;
	float *pCudaResult = 0;
	int i;

	// reserve memory in host system
	pHostArgument = (float *)malloc(N*sizeof(pHostArgument[0]));
	pHostResult = (float *) malloc(N*sizeof(pHostResult[0]));

	// reserve memory in cuda
	cudaMalloc((void **) &pCudaArgument, N*sizeof(pCudaResult[0]));
	cudaMalloc((void **) &pCudaResult, N*sizeof(pCudaResult[0]));

	// initialize argument
	for (i = 0; i < N; i++) pHostArgument[i] = float(i);

	// copy argument from host to cuda
	cudaMemcpy(	pCudaArgument, 				// destination
				pHostArgument, 				// source
				N*sizeof(pCudaResult[0]),	// amount to copy
				cudaMemcpyHostToDevice);	// type: host -> device

	// execute in cuda
	cudaFunct<<<1,SIM_THREADS>>>(pCudaArgument, pCudaResult);

	// copy result from cuda to host
	cudaMemcpy(	pHostResult, 				// destination
				pCudaResult, 				// source
				N*sizeof(pCudaResult[0]),	// amount to copy
				cudaMemcpyDeviceToHost);	// type: device -> host

	for (i = 0; i < N; i++)
		printf("%f\n", pHostResult[i]);
}

