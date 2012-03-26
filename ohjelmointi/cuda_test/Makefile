
flags=-I /Developer/GPU_Computing/C/common/inc/ /Developer/GPU_Computing/C/lib/libcutil_i386.a

all:: #convolution simpleCuda.cu simpleCuda2.cu simpleCuda3.cu simpleCuda4.cu 
	nvcc ${flags} src/convolution/convolution.cu -o convolution

convolution:
	@echo "  [cc] " $@
	@nvcc   ${flags} src/convolution/$@.cu -o $@
	
	
%.cu:: %
	@echo "  [cc] " $^
	@nvcc ${flags} src/simple/$@ -o $^
	

clean:
	rm -f convolution

