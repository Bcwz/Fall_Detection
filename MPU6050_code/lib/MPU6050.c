#include <stdio.h>
#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>
#include <ctype.h>
#include <poll.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/time.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/ioctl.h>
#include <asm/ioctl.h>

#include "MPU6050.h"

#define I2C_SLAVE	                0x0703
#define I2C_SMBUS	                0x0720

#define I2C_SMBUS_READ	            	1
#define I2C_SMBUS_WRITE	            	0

#define I2C_SMBUS_QUICK		        0
#define I2C_SMBUS_BYTE		        1
#define I2C_SMBUS_BYTE_DATA	        2 
#define I2C_SMBUS_WORD_DATA	        3
#define I2C_SMBUS_PROC_CALL	        4
#define I2C_SMBUS_BLOCK_DATA	    	5
#define I2C_SMBUS_I2C_BLOCK_BROKEN  	6
#define I2C_SMBUS_BLOCK_PROC_CALL   	7
#define I2C_SMBUS_I2C_BLOCK_DATA    	8

#define I2C_SMBUS_BLOCK_MAX	        32

union i2c_smbus_data
{
  uint8_t  byte ;
  uint16_t word ;
  uint8_t  block [I2C_SMBUS_BLOCK_MAX + 2] ;	// block [0] is used for length + one more for PEC
} ;

// smbus ioctl
struct i2c_smbus_ioctl_data
{
  char read_write ;
  uint8_t command ;
  int size ;
  union i2c_smbus_data *data ;
} ;

static inline int i2c_smbus_access (int fd, char rw, uint8_t command, int size, union i2c_smbus_data *data)
{
  struct i2c_smbus_ioctl_data args ;

  args.read_write = rw ;
  args.command    = command ;
  args.size       = size ;
  args.data       = data ;
  return ioctl (fd, I2C_SMBUS, &args) ;
}

// register read
int I2CReadReg8 (int fd, int reg)
{
  union i2c_smbus_data data;

  if (i2c_smbus_access (fd, I2C_SMBUS_READ, reg, I2C_SMBUS_BYTE_DATA, &data))
    return -1 ;
  else
    return data.byte & 0xFF ;
}

// gpio layout
int piGpioLayout (void)
{
  static int  gpioLayout = -1 ;

  if (gpioLayout != -1)
    return gpioLayout ;
}

// I2C setup interface
int I2CSetupInterface (const char *device, int devId)
{
  int fd ;
  
  fd = open (device, O_RDWR);
  
  ioctl (fd, I2C_SLAVE, devId);
  
  return fd ;
}

// setup I2C
int I2CSetup (const int devId)
{
  int rev ;
  const char *device ;

  rev = piGpioLayout () ;

  if (rev == 1)
    device = "/dev/i2c-0" ;
  else
    device = "/dev/i2c-1" ;

  return I2CSetupInterface (device, devId) ;
}

// return fd to be used when reading data
int getFd(const int Device_Address) {
	return I2CSetup(Device_Address); // setup MPU6050 address
}

// read and calc accelerometer
float readAcc(int fd, int addr) {
	short high_byte, low_byte, value;           // for raw data
	high_byte = I2CReadReg8(fd, addr);          // get raw value
	low_byte = I2CReadReg8(fd, addr+1);         // get raw value
	value = (high_byte << 8) | low_byte;        // combine raw values with OR
	return (float) value/16384.0;               // calculate acceleration
}

// read and calc gyrometer
float readGyro(int fd, int addr) {
	short high_byte, low_byte, value;           // for raw data
	high_byte = I2CReadReg8(fd, addr);          // get raw value
	low_byte = I2CReadReg8(fd, addr+1);         // get raw value
	value = (high_byte << 8) | low_byte;        // combine raw values with OR
	return (float) value/131.0;                 // calculate acceleration
}
