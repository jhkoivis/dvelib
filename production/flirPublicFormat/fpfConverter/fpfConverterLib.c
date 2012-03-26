
#include "fpfConverterLib.h"

void readCamData(	FPFHEADER_T *fpfHeader,
					char *outputString)
{
	outputString[0] = '\0';
	SPRINT_KEY( "# camera_name        : %s\n", camData.camera_name )
	SPRINT_KEY( "# camera_partn       : %s\n", camData.camera_partn )
	SPRINT_KEY( "# camera_sn          : %s\n", camData.camera_sn )

	//printf('%c', camData.ca)

	SPRINT_KEY( "# camera_range_tmin  : %f\n", camData.camera_range_tmin )
	SPRINT_KEY( "# camera_range_tmax  : %f\n", camData.camera_range_tmax )
	SPRINT_KEY( "# lens_name          : %s\n", camData.lens_name )
	SPRINT_KEY( "# lens_partn         : %s\n", camData.lens_partn )
	SPRINT_KEY( "# lens_sn            : %s\n", camData.lens_sn )
	SPRINT_KEY( "# filter_name        : %s\n", camData.filter_name )
	SPRINT_KEY( "# filter_partn       : %s\n", camData.filter_partn )
	SPRINT_KEY( "# filter_sn          : %s\n", camData.filter_sn )

}

void readObjPar(	FPFHEADER_T *fpfHeader,
					char *outputString)
{
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
					char *outputString)
{
	outputString[0] = '\0';
	SPRINT_KEY( "# tMinCam            : %f\n", scaling.tMinCam )
	SPRINT_KEY( "# tMaxcam            : %f\n", scaling.tMaxCam )
	SPRINT_KEY( "# tMinCalc           : %f\n", scaling.tMinCalc )
	SPRINT_KEY( "# tMaxCalc           : %f\n", scaling.tMaxCalc )
	SPRINT_KEY( "# tMinScale          : %f\n", scaling.tMinScale )
	SPRINT_KEY( "# tMaxScale          : %f\n", scaling.tMaxScale )
}

void writeConversionInfo(	char *outputString,
							float *tMin,
							float *tMax)
{
	outputString[0] = '\0';
	sprintf(&outputString[strlen(outputString)], 
			"# conversion_0_in_kelvins             : %f\n",
			*tMin);
	sprintf(&outputString[strlen(outputString)], 
			"# conversion_%d_in_kelvins         : %f\n",
			PGM_MAX_VALUE,
			*tMax);
	sprintf(&outputString[strlen(outputString)], 
			"# conversion_0_in_celcius             : %f\n",
			*tMin - DEGREE_0);
	sprintf(&outputString[strlen(outputString)], 
			"# conversion_%d_in_celsius         : %f\n",
			PGM_MAX_VALUE,
			*tMax - DEGREE_0);
}

void readImgData(	FPFHEADER_T *fpfHeader,
					char *outputString)
{
	int i;
	outputString[0] = '\0';
	sprintf(&outputString[strlen(outputString)], 
			"# fpfID                  : %s\n",
			fpfHeader->imgData.fpfID);
	sprintf(&outputString[strlen(outputString)],
			"# version                : %lu\n",
			fpfHeader->imgData.version);
	sprintf(&outputString[strlen(outputString)], 
			"# pixelOffset            : %lu\n",
			fpfHeader->imgData.pixelOffset);
	sprintf(&outputString[strlen(outputString)],
			"# ImageType              : %hu\n",
			fpfHeader->imgData.ImageType);
	sprintf(&outputString[strlen(outputString)], 
			"# pixelFormat            : %hu\n",
			fpfHeader->imgData.pixelFormat);
	sprintf(&outputString[strlen(outputString)],
			"# xSize                  : %hu\n",
			fpfHeader->imgData.xSize);
	sprintf(&outputString[strlen(outputString)], 
			"# ySize                  : %hu\n",
			fpfHeader->imgData.ySize);
	sprintf(&outputString[strlen(outputString)],
			"# trig_count             : %lu\n",
			fpfHeader->imgData.trig_count);
	sprintf(&outputString[strlen(outputString)],
			"# frame_count            : %lu\n",
			fpfHeader->imgData.trig_count);
	sprintf(&outputString[strlen(outputString)],
			"# spareLong              : ");
	for (i = 0; i < 16; i++)
	{
		sprintf(&outputString[strlen(outputString)],
				"%lu,",
				fpfHeader->imgData.spareLong[i]);
	}
	sprintf(&outputString[strlen(outputString)], "\n");
}

void makeHeader(	FPFHEADER_T *fpfHeader,
					char *header,
					float *tMin,
					float *tMax)
{
	char 	reUsableHeader[MAX_STRING_SIZE];
	
	header[0] = '\0';
	sprintf(header, "P2\n");
	readImgData(fpfHeader, reUsableHeader);
	sprintf(&header[strlen(header)], "%s", reUsableHeader);
	readCamData(fpfHeader, reUsableHeader);
	sprintf(&header[strlen(header)], "%s", reUsableHeader);
	readObjPar(fpfHeader, reUsableHeader);
	sprintf(&header[strlen(header)], "%s", reUsableHeader);
	readDateTime(fpfHeader, reUsableHeader);
	sprintf(&header[strlen(header)], "%s", reUsableHeader);
	readScaling(fpfHeader, reUsableHeader);
	sprintf(&header[strlen(header)], "%s", reUsableHeader);
	writeConversionInfo(reUsableHeader, tMin, tMax);
	sprintf(&header[strlen(header)], "%s", reUsableHeader);
	

	sprintf(&header[strlen(header)], "320 240\n");
	sprintf(&header[strlen(header)], "%d\n", PGM_MAX_VALUE);
	
}

void makeData(		FILE *pFpfFile, 
					float *fpfData, 
					int *maxFloatCount)
{
	float data;
	
	*maxFloatCount = 0;
	fread(&data, 1, sizeof(float), pFpfFile);
	while (!feof(pFpfFile)) {
		fpfData[*maxFloatCount] = data;
		(*maxFloatCount)++;
		fread(&data, 1, sizeof(float), pFpfFile);
	}
}


