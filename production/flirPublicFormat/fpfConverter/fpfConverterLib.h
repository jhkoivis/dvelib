
#ifndef FPFCONVERTERLIB_H
#define FPFCONVERTERLIB_H

#include "Fpfimg.h"
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>

#define MAX_STRING_SIZE 	10000000			// max header size
#define MAX_FLOAT_ARRAY		10000000	
#define DEGREE_0 			273.15
#define PGM_MAX_VALUE		65535
#define SPRINT_KEY( X, Y) 	sprintf(&outputString[strlen(outputString)], X, fpfHeader->Y);

/*
 * Writes lines:
 *   # conversion_0_in_kelvins     : 290.15
 *   # conversion_65535_in_kelvins : 390.15
 *   # conversion_0_in_degrees     : 0
 *   # conversion_65535_in_degrees : 100
 */
void writeConversionInfo(	char *outputString,	//<-- write data here
							float *tMin,			//<-- value 0 in image data
												//    coresponds tMin kelvins
							float *tMax);		//<-- value PGN_MAX_VALUE in
												//    image data corresponds 
												//	  tMax kelvins
												
												
void readImgData(	FPFHEADER_T *fpfHeader,		//<-- header struct to decode
					char *outputString);		//<-- string to write the data
					
void readCamData(	FPFHEADER_T *fpfHeader,
					char *outputString);
					
void readObjPar(	FPFHEADER_T *fpfHeader,
					char *outputString);

void readDateTime(	FPFHEADER_T *fpfHeader,
					char *outputString);


void readScaling(	FPFHEADER_T *fpfHeader,
					char *outputString);
					
void makeHeader(	FPFHEADER_T *fpfHeader,
					char *outputString,
					float *tMin,
					float *tMax);
					
void makeData(		FILE *pFpfFile, 
					float *fpfData, 
					int *maxFloatCount);	
					
#endif





