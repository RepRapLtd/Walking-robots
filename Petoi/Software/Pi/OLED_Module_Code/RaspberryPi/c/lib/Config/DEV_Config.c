/*****************************************************************************
* | File      	:   DEV_Config.c
* | Author      :   Waveshare team
* | Function    :   Hardware underlying interface
* | Info        :
*----------------
* |	This version:   V2.0
* | Date        :   2020-06-17
* | Info        :   Basic version
*
******************************************************************************/
#include "DEV_Config.h"
#include <unistd.h>

uint32_t fd;
/*****************************************
                GPIO
*****************************************/
void DEV_Digital_Write(UWORD Pin, UBYTE Value)
{
#ifdef USE_BCM2835_LIB
    bcm2835_gpio_write(Pin, Value);
    
#elif USE_WIRINGPI_LIB
    digitalWrite(Pin, Value);
    
#elif USE_DEV_LIB
    SYSFS_GPIO_Write(Pin, Value);
    
#endif
}

UBYTE DEV_Digital_Read(UWORD Pin)
{
    UBYTE Read_value = 0;
#ifdef USE_BCM2835_LIB
    Read_value = bcm2835_gpio_lev(Pin);
    
#elif USE_WIRINGPI_LIB
    Read_value = digitalRead(Pin);
    
#elif USE_DEV_LIB
    Read_value = SYSFS_GPIO_Read(Pin);
#endif
    return Read_value;
}

void DEV_GPIO_Mode(UWORD Pin, UWORD Mode)
{
#ifdef USE_BCM2835_LIB  
    if(Mode == 0 || Mode == BCM2835_GPIO_FSEL_INPT){
        bcm2835_gpio_fsel(Pin, BCM2835_GPIO_FSEL_INPT);
    }else {
        bcm2835_gpio_fsel(Pin, BCM2835_GPIO_FSEL_OUTP);
    }
#elif USE_WIRINGPI_LIB
    if(Mode == 0 || Mode == INPUT){
        pinMode(Pin, INPUT);
        pullUpDnControl(Pin, PUD_UP);
    }else{ 
        pinMode(Pin, OUTPUT);
        // printf (" %d OUT \r\n",Pin);
    }
#elif USE_DEV_LIB
    SYSFS_GPIO_Export(Pin);
    if(Mode == 0 || Mode == SYSFS_GPIO_IN){
        SYSFS_GPIO_Direction(Pin, SYSFS_GPIO_IN);
        // printf("IN Pin = %d\r\n",Pin);
    }else{
        SYSFS_GPIO_Direction(Pin, SYSFS_GPIO_OUT);
        // printf("OUT Pin = %d\r\n",Pin);
    }
#endif   
}

/**
 * delay x ms
**/
void DEV_Delay_ms(UDOUBLE xms)
{
#ifdef USE_BCM2835_LIB
    bcm2835_delay(xms);
#elif USE_WIRINGPI_LIB
    delay(xms);
#elif USE_DEV_LIB
    UDOUBLE i;
    for(i=0; i < xms; i++){
        usleep(1000);
    }
#endif
}

static void DEV_GPIO_Init(void)
{
    DEV_GPIO_Mode(OLED_CS, 1);
    DEV_GPIO_Mode(OLED_RST, 1);
    DEV_GPIO_Mode(OLED_DC, 1);
}

/******************************************************************************
function:	Module Initialize, the library and initialize the pins, SPI protocol
parameter:
Info:
******************************************************************************/
UBYTE DEV_ModuleInit(void)
{
	
 #ifdef USE_BCM2835_LIB
    if(!bcm2835_init()) {
        printf("bcm2835 init failed  !!! \r\n");
        return 1;
    } else {
        printf("bcm2835 init success !!! \r\n");
    }
	DEV_GPIO_Init();
    #if USE_SPI
        printf("USE_SPI\r\n");  
        bcm2835_spi_begin();                                         //Start spi interface, set spi pin for the reuse function
        bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);     //High first transmission
        bcm2835_spi_setDataMode(BCM2835_SPI_MODE3);                  //spi mode 3
        bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_128);  //Frequency
        bcm2835_spi_chipSelect(BCM2835_SPI_CS0);                     //set CE0
        bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);     //enable cs0
    #elif USE_IIC
        OLED_DC_0;
        OLED_CS_0;
        printf("USE_IIC\r\n");
        bcm2835_i2c_begin();	
        bcm2835_i2c_setSlaveAddress(0x3c);
         /**********************************************************/
    #endif
    
#elif USE_WIRINGPI_LIB  
    //if(wiringPiSetup() < 0) {//use wiringpi Pin number table  
    if(wiringPiSetupGpio() < 0) { //use BCM2835 Pin number table
        printf("set wiringPi lib failed	!!! \r\n");
        return 1;
    } else {
        printf("set wiringPi lib success  !!! \r\n");
    }
	DEV_GPIO_Init();
    #if USE_SPI
        printf("USE_SPI\r\n");       
        //wiringPiSPISetup(0,9000000);
        wiringPiSPISetupMode(0, 9000000, 3);
    #elif USE_IIC
        OLED_DC_0;
        OLED_CS_0;
        printf("USE_IIC\r\n");
        fd = wiringPiI2CSetup(0x3c);
    #endif
   
#elif USE_DEV_LIB
	DEV_GPIO_Init();
    #if USE_SPI
        printf("USE_SPI\r\n"); 
        DEV_HARDWARE_SPI_begin("/dev/spidev0.0");
		DEV_HARDWARE_SPI_Mode(SPI_MODE_3);
    #elif USE_IIC   
        printf("USE_IIC\r\n");		
        OLED_DC_0;
        OLED_CS_0;
        DEV_HARDWARE_I2C_begin("/dev/i2c-1");
        DEV_HARDWARE_I2C_setSlaveAddress(0x3c);
    #endif
#endif
    return 0;
}

void DEV_SPI_WriteByte(uint8_t Value)
{
#ifdef USE_BCM2835_LIB
    bcm2835_spi_transfer(Value);
    
#elif USE_WIRINGPI_LIB
    wiringPiSPIDataRW(0,&Value,1);
    
#elif USE_DEV_LIB
	// printf("write data is %d\r\n", Value);
    DEV_HARDWARE_SPI_TransferByte(Value);
    
#endif
}

void DEV_SPI_Write_nByte(uint8_t *pData, uint32_t Len)
{
	printf("data is %s", pData);
#ifdef USE_BCM2835_LIB
    char rData[Len];
    bcm2835_spi_transfernb(pData,rData,Len);
    
#elif USE_WIRINGPI_LIB
    wiringPiSPIDataRW(0, pData, Len);
    
#elif USE_DEV_LIB
    DEV_HARDWARE_SPI_Transfer(pData, Len);
    
#endif
}

void I2C_Write_Byte(uint8_t value, uint8_t Cmd)
{
#ifdef USE_BCM2835_LIB
    char wbuf[2]={Cmd, value};
    bcm2835_i2c_write(wbuf, 2);
#elif USE_WIRINGPI_LIB
	int ref;
	//wiringPiI2CWrite(fd,Cmd);
    ref = wiringPiI2CWriteReg8(fd, (int)Cmd, (int)value);
    while(ref != 0) {
        ref = wiringPiI2CWriteReg8 (fd, (int)Cmd, (int)value);
        if(ref == 0)
            break;
    }
#elif USE_DEV_LIB
    char wbuf[2]={Cmd, value};
    DEV_HARDWARE_I2C_write(wbuf, 2);

#endif
}

/******************************************************************************
function:	Module exits, closes SPI and BCM2835 library
parameter:
Info:
******************************************************************************/
void DEV_ModuleExit(void)
{
#ifdef USE_BCM2835_LIB
    bcm2835_spi_end();
	bcm2835_i2c_end();
    bcm2835_close();


#elif USE_WIRINGPI_LIB
    OLED_CS_0;
	OLED_RST_1;
	OLED_DC_0;

#elif USE_DEV_LIB
    OLED_CS_0;
	OLED_RST_1;
	OLED_DC_0;
    DEV_HARDWARE_SPI_end();
    DEV_HARDWARE_I2C_end();
#endif
}

