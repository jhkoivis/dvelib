/* Cuda GPU Based Program that use GPU processor for finding cosine of numbers */

/* --------------------------- header secton ----------------------------*/
#include<stdio.h>
#include<cuda.h>

#define COS_THREAD_CNT 2
#define N 10

/* --------------------------- target code ------------------------------*/
struct cosParams {
	float *arg;
	float *res;
	int n;
	//int *threadIdx;
};

__global__ void cos_main(struct cosParams parms)
{
	int i;
	for (i = threadIdx.x; i < parms.n; i += COS_THREAD_CNT)
	{
		parms.res[i] = __cosf(parms.arg[i] );
		//parms.threadIdx[0] = (int)threadIdx.x;
	}
}

/* --------------------------- host code ------------------------------*/
int main (int argc, char *argv[])
{
	int 			i = 0;
	cudaError_t 	cudaStat;
	//int*			cosThreadIdx = 0;
	float* 			cosRes = 0;
	float*			cosArg = 0;
	//int*			threadIdx = (int *) malloc(N*sizeof(threadIdx));
	float* 			arg = (float *) malloc(N*sizeof(arg[0]));
	float*			res = (float *) malloc(N*sizeof(res[0]));
	struct cosParams funcParams;


	/* ... fill arguments array "arg" .... */
	for(i=0; i < N; i++ ){
		arg[i] = (float)i;
	}

	cudaStat = cudaMalloc ((void **)&cosArg, 	N * sizeof(cosArg[0]));
	cudaStat = cudaMalloc ((void **)&cosRes, 	N * sizeof(cosRes[0]));
	//cudaStat = cudaMalloc ((void **)&threadIdx, N * sizeof(threadIdx[0]));
	cudaStat = cudaMemcpy (	cosArg,
							arg,
							N * sizeof(arg[0]),
							cudaMemcpyHostToDevice);

	funcParams.res = cosRes;
	funcParams.arg = cosArg;
	funcParams.n = N;
	//funcParams.threadIdx = cosThreadIdx;
	cos_main<<<1,COS_THREAD_CNT>>>(funcParams);

	cudaStat = cudaMemcpy(	res,
							cosRes,
							N * sizeof(cosRes[0]),
							cudaMemcpyDeviceToHost);

	//cudaStat = cudaMemcpy(	threadIdx,
	//						cosThreadIdx,
	//						N * sizeof(cosThreadIdx[0]),
	//						cudaMemcpyDeviceToHost);

	for(i=0; i < N; i++ )
	{
		printf("%d: cosf(%f) = %f\n", arg[i], res[i]); //, threadIdx[i]);
	}
}

/* nvcc cosine.cu -use_fast_math */
