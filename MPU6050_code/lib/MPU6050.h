#ifndef MPU6050_H
#define MPU6050_H

int getFd(const int Device_Address);
float readAcc(int fd, int addr);
float readGyro(int fd, int addr);

#endif
