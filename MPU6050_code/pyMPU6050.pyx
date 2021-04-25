cdef extern from "MPU6050.h":
    int getFd(const int Device_Address)
    float readAcc(int fd, int addr)
    float readGyro(int fd, int addr)
    
def py_getFd(Device_Address: int) -> int:
    return getFd(Device_Address)
    
def py_readAcc(fd: int, addr: int) -> float:
    return readAcc(fd, addr)
    
def py_readGyro(fd: int, addr: int) -> float:
    return readGyro(fd, addr)
    