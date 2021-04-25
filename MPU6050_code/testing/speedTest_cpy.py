import smbus        # import SMBus module of I2C
import time         # import time modules
import pyMPU6050    # import C funtions for measuring MPU6050

# addresses for MPU6050 registers
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACC_X_ADDR   = 0x3B
ACC_Y_ADDR   = 0x3D
ACC_Z_ADDR   = 0x3F
GYRO_X_ADDR  = 0x43
GYRO_Y_ADDR  = 0x45
GYRO_Z_ADDR  = 0x47

def MPU_Init():
    # write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    # write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    # write to configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    # write to gyroscope configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    # write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)
    
    
# -- Main Program -- #

bus = smbus.SMBus(1)                     # map smbus for initialization
Device_Address = 0x68                    # MPU6050 device address
MPU_Init()                               # call initializer
fd = pyMPU6050.py_getFd(Device_Address)  # set-up device address for C functions

n = 1000 * 10
i = 0

print ("Tracking user movement")         # indicate prediction start

startTime = int(round(time.time()*1000))

while i < n:
    # get calculated accelerometer values
    acc_x = pyMPU6050.py_readAcc(fd, ACC_X_ADDR)
    acc_y = pyMPU6050.py_readAcc(fd, ACC_Y_ADDR)
    acc_z = pyMPU6050.py_readAcc(fd, ACC_Z_ADDR)  
    # get calculated gyroscope values
    gyro_x = pyMPU6050.py_readGyro(fd, GYRO_X_ADDR)
    gyro_y = pyMPU6050.py_readGyro(fd, GYRO_Y_ADDR)
    gyro_z = pyMPU6050.py_readGyro(fd, GYRO_Z_ADDR)
    # print out values for testing
    print ("Gx=%.2f" %gyro_x, u'\u00b0'+ "/s", "\tGy=%.2f" %gyro_y, u'\u00b0'+ "/s", "\tGz=%.2f" %gyro_z, u'\u00b0'+ "/s", "\tAx=%.2f g" %acc_x, "\tAy=%.2f g" %acc_y, "\tAz=%.2f g" %acc_z)
    # time.sleep(1)
    # i += 1

endTime = int(round(time.time()*1000))
print((endTime - startTime)/10)