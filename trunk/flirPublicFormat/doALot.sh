#!/bin/sh

for file in `ls /archive/csm/jko/infrared/$1/*.FPF`; do 
	dir=${file%/*}
	newFpf=`python fpfConverter/rename.py ${file##*/}`
	echo mv $file $dir/$newFpf 
	echo fpfConverter/fpfConverter $dir/$newFpf $dir/$newFpf.pgm;
	echo bzip2 $dir/$newFpf
done 
