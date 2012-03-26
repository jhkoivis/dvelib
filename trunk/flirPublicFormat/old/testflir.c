
/*
 * NOTE! this code works only in 32bit machines
 * unsigned long (or "%lu") has a different length 
 * 
 * TODO: 
 * - readCamData has problems with empty strings FIXIT 
 * 
*/

#include "Fpfimg.h"
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>

#define MAX_STRING_SIZE 	10000000
#define MAX_FLOAT_ARRAY		10000000
#define DEGREE_0 			273.15
#define PGN_MAX_VALUE		65536
#define SPRINT_KEY( X, Y) 	sprintf(&outputString[strlen(outputString)], X, fpfHeader->Y);


void writeConversionInfo(	char *outputString,
							float tMin,
							float tMax)
{
	outputString[0] = '\0';
	sprintf(&outputString[strlen(ouputString)], 
			'# conversion_0_in_kelvins : %f', 
			tMin);
	sprintf(&outputString[strlen(ouputString)], 
			'# conversion_PGN_MAX_VALUE_in_kelvins : %f', 
			tMax);
	sprintf(&outputString[strlen(ouputString)], 
			'# conversion_0_in_celcius : %f', 
			tMin - DEGREE_0);
	sprintf(&outputString[strlen(ouputString)], 
			'# conversion_PGN_MAX_VALUE_in_celsius : %f', 
			tMax -DEGREE_0);
	
}

void readImgData(	FPFHEADER_T *fpfHeader,
					char *outputString)
{
	int i;
	outputString[0] = '\0';
	sprintf(&outputString[strlen(outputString)], 
			"# fpfID         : %s\n",
			fpfHeader->imgData.fpfID);
	sprintf(&outputString[strlen(outputString)],
			"# version       : %lu\n",
			fpfHeader->imgData.version);
	sprintf(&outputString[strlen(outputString)], 
			"# pixelOffset   : %lu\n",
			fpfHeader->imgData.pixelOffset);
	sprintf(&outputString[strlen(outputString)],
			"# ImageType     : %hu\n",
			fpfHeader->imgData.ImageType);
	sprintf(&outputString[strlen(outputString)], 
			"# pixelFormat   : %hu\n",
			fpfHeader->imgData.pixelFormat);
	sprintf(&outputString[strlen(outputString)],
			"# xSize         : %hu\n",
			fpfHeader->imgData.xSize);
	sprintf(&outputString[strlen(outputString)], 
			"# ySize         : %hu\n",
			fpfHeader->imgData.ySize);
	sprintf(&outputString[strlen(outputString)],
			"# trig_count    : %lu\n",
			fpfHeader->imgData.trig_count);
	sprintf(&outputString[strlen(outputString)],
			"# frame_count   : %lu\n",
			fpfHeader->imgData.trig_count);
	sprintf(&outputString[strlen(outputString)],
				"# spareLong     : ");		
	for (i = 0; i < 16; i++)
	{
		sprintf(&outputString[strlen(outputString)],
				"%lu,",
				fpfHeader->imgData.spareLong[i]);
	}
	sprintf(&outputString[strlen(outputString)], "\n");
}


void readCamData(	FPFHEADER_T *fpfHeader,
					char *outputString)
{
	int i;
	outputString[0] = '\0';
	SPRINT_KEY( "# camera_name        : %s\n", camData.camera_name )
	SPRINT_KEY( "# camera_partn       : %s\n", camData.camera_partn )
	SPRINT_KEY( "# camera_sn          : %s\n", camData.camera_sn )
	/*
	SPRINT_KEY( "# camera_range_tmin  : %s", camData.camera_range_tmin )
	SPRINT_KEY( "# camera_range_tmax  : %s", camData.camera_range_tmax )
	SPRINT_KEY( "# lens_name          : %s", camData.lens_name )
	SPRINT_KEY( "# lens_partn         : %s", camData.lens_partn )
	SPRINT_KEY( "# lens_sn            : %s", camData.lens_sn )
	SPRINT_KEY( "# filter_name        : %s", camData.filter_name )
	SPRINT_KEY( "# filter_partn       : %s", camData.filter_partn )
	SPRINT_KEY( "# filter_sn          : %s", camData.filter_sn )
	*/
}

void readObjPar(	FPFHEADER_T *fpfHeader,
					char *outputString)
{
	int i;
	outputString[0] = '\0';
	SPRINT_KEY( "# emissivity         : %f\n", objPar.emissivity )
	SPRINT_KEY( "# objectDistance     : %f\n", objPar.objectDistance )
	SPRINT_KEY( "# ambTemp            : %f\n", objPar.ambTemp )
	SPRINT_KEY( "# atmTemp            : %f\n", objPar.atmTemp )
	SPRINT_KEY( "# relHum             : %f\n", objPar.relHum )
	SPRINT_KEY( "# compuTao           : %f\n", objPar.compuTao )
	SPRINT_KEY( "# estimTao           : %f\n", objPar.estimTao )
	SPRINT_KEY( "# refTemp            : %f\n", objPar.refTemp )
	SPRINT_KEY( "# extOptTemp         : %f\n", objPar.extOptTemp )
	SPRINT_KEY( "# extOptTrans        : %f\n", objPar.extOptTrans )
	
}

void readDateTime(	FPFHEADER_T *fpfHeader,
					char *outputString)
{
	int i;
	outputString[0] = '\0';
	SPRINT_KEY( "# Year               : %d\n", datetime.Year )
	SPRINT_KEY( "# Month              : %d\n", datetime.Month )
	SPRINT_KEY( "# Day                : %d\n", datetime.Day )
	SPRINT_KEY( "# Hour               : %d\n", datetime.Hour )
	SPRINT_KEY( "# Minute             : %d\n", datetime.Minute )
	SPRINT_KEY( "# Second             : %d\n", datetime.Second )
	SPRINT_KEY( "# MilliSecond        : %d\n", datetime.MilliSecond )
}

void readScaling(	FPFHEADER_T *fpfHeader,
					char *outputString,
					float *tMinScale,
					float *tMaxScale)
{
	int i;
	outputString[0] = '\0';
	SPRINT_KEY( "# tMinCam            : %f\n", scaling.tMinCam )
	SPRINT_KEY( "# tMaxcam            : %f\n", scaling.tMaxCam )
	SPRINT_KEY( "# tMinCalc           : %f\n", scaling.tMinCalc )
	SPRINT_KEY( "# tMaxCalc           : %f\n", scaling.tMaxCalc )
	SPRINT_KEY( "# tMinScale          : %f\n", scaling.tMinScale )
	SPRINT_KEY( "# tMaxScale          : %f\n", scaling.tMaxScale )
	
	tMinScale[0] = fpfHeader->scaling.tMinScale;
	tMaxScale[0] = fpfHeader->scaling.tMaxScale;	

}



int main(int argc, char *argv[])
/*
 * Read fpf file as argument 1 and save pgm file as argument 2.
 * 
 * - Header to header, data to image.
 * - add: 
 * 		minT : min(temperature)
 * 		maxT : max(temperature)
 * - scale:
 * 		minT -> 0
 * 		maxT -> 2^16 = 65536
 * 
 * */
{
	char 	*pFpfFn,
			*pPgnFn,
			reUsableHeader[MAX_STRING_SIZE];
	FILE 	*pFpfFile,
			*pPgnFile;
	FPFHEADER_T 
			fpfHeader;
	float	data,
			tMin,
			tMax;
	int 	dataInt;
	
	if (argc != 3){
		printf("usage:\n  %s inFile.fpf outFile.pgn\n", argv[0]);
		return 1;
	}
	 
	pFpfFn = argv[1];
	pPgnFn = argv[2];
	
	printf(	"\n  reading: %s\n  saving:  %s\n",
			pFpfFn,
			pPgnFn);
	
	pFpfFile = fopen(pFpfFn,"r");
	pPgnFile = fopen(pPgnFn, "w");
	
	fread(&fpfHeader, sizeof(FPFHEADER_T), 1, pFpfFile);

	fprintf(pPgnFile, "P2\n");
	
	readImgData(&fpfHeader, reUsableHeader);
	fprintf(pPgnFile, "%s", reUsableHeader);
	readCamData(&fpfHeader, reUsableHeader);
	fprintf(pPgnFile, "%s", reUsableHeader);
	readObjPar(&fpfHeader, reUsableHeader);
	fprintf(pPgnFile, "%s", reUsableHeader);
	readDateTime(&fpfHeader, reUsableHeader);
	fprintf(pPgnFile, "%s", reUsableHeader);
	readScaling(&fpfHeader, reUsableHeader,
				&tMin, &tMax);
	fprintf(pPgnFile, "%s", reUsableHeader);
	
	fprintf(pPgnFile, "320 240\n");
	fprintf(pPgnFile, "65536\n");
	
	fread(&data, 1,sizeof(float),pFpfFile);
	while (!feof(pFpfFile)) {
		data = 65536.0*(data - tMin)/(tMax-tMin);
		dataInt = (int)(data + 0.5);
		fprintf(pPgnFile, "%d\n", dataInt);
		fread(&data, 1,sizeof(float),pFpfFile);
	}
	return 0; 
	
}


