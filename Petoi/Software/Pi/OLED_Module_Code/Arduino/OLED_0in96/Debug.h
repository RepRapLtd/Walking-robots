/*****************************************************************************
* | File      	:	Debug.h
* | Author      : Waveshare team
* | Function    :	debug with printf
* | Info        :
*----------------
* |	This version:   V1.0
* | Date        :   2020-06-16
* | Info        :   Basic version
*
******************************************************************************/
#ifndef __DEBUG_H
#define __DEBUG_H

#include "stdio.h"

#define DEBUG 0 //No enough memory
#if DEBUG
	#define Debug(__info,...) printf("Debug : " __info,##__VA_ARGS__)
#else
	#define Debug(__info,...)  
#endif

#endif
