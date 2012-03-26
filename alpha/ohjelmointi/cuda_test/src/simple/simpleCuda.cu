
#include <stdio.h>
#include <cuda.h>

#define	SIM_THREADS		10		// how many simultaneus threads
#define N	100					// number of variables in a vector


// this function does absolutely nothing, but runs on multiple cores
__global__ void dummyFunct(void)
{
	int i;
	int a = 0;

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
		a += 1;
}

int main(void)
{
	dummyFunct<<<1,SIM_THREADS>>>();
}


