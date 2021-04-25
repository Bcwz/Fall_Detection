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
    
def start_csv():
    outputFile = open('data.csv', 'w')
    outputFile.write("g_x,g_y,g_z,a_x,a_y,a_z,target\n")
    
def write_to_csv(gx, gy, gz, ax, ay, az, target):
    outputFile = open('data.csv', 'a')
    datawrite = str(gx) + "," + str(gy) + "," + str(gz) + "," + str(ax) + "," + str(ay) + "," + str(az) + "," + str(target) + "\n"
    print(datawrite)
    outputFile.write(datawrite)
    
# -- Main Program -- #

bus = smbus.SMBus(1)                     # map smbus for initialization
Device_Address = 0x68                    # MPU6050 device address
MPU_Init()                               # call initializer
fd = pyMPU6050.py_getFd(Device_Address)  # set-up device address for C functions

print ("Tracking user movement")         # indicate prediction start

print ("5")
time.sleep(1)
print ("4")
time.sleep(1)
print ("3")
time.sleep(1)
print ("2")
time.sleep(1)
print ("1")
time.sleep(1)

start_csv()
while True:
    # get calculated accelerometer values
    acc_x = pyMPU6050.py_readAcc(fd, ACC_X_ADDR)
    acc_y = pyMPU6050.py_readAcc(fd, ACC_Y_ADDR)
    acc_z = pyMPU6050.py_readAcc(fd, ACC_Z_ADDR)  
    # get calculated gyroscope values
    gyro_x = pyMPU6050.py_readGyro(fd, GYRO_X_ADDR)
    gyro_y = pyMPU6050.py_readGyro(fd, GYRO_Y_ADDR)
    gyro_z = pyMPU6050.py_readGyro(fd, GYRO_Z_ADDR)
    # print out values for testing
    
    write_to_csv (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, 0)
    
