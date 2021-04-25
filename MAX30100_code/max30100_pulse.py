import smbus
import time

''' Registers '''
MAX30100_ADDR = 0x57 #MAX30100 Pulse i2c Address

#Interrupt
INTERRUPT_STATUS = 0x00
INTERRUPT_ENABLE = 0x01

#FIFO
FIFO_DATA_REGISTER = 0x05

#Modes Configuration
MODE_CONFIGURATION = 0x06
SPO2_CONFIGURATION = 0x07
LED_CONFIGURATION = 0x09

#Modes
MODE_HR = 0x02
MODE_SPO2 = 0x03

#Temperature
TEMP_INTEGER = 0x16
TEMPERATURE_DECIMAL= 0x17

#LED_BRIGHTNESS
LED_27_CURRENT = 0x08

#Pulse Width
PULSE_WIDTH = 1600

class MAX30100(object):
    
    def __init__(self):
        self.i2c = smbus.SMBus(1)
        self.current_ir = 0
        self.current_red = 0
        self.max_length = 10000
        
        #Set Mode to SPO2
        self.i2c.write_byte_data(MAX30100_ADDR, MODE_CONFIGURATION, MODE_SPO2)

        #Set the LED Current
        self.i2c.write_byte_data(MAX30100_ADDR, LED_CONFIGURATION, (LED_27_CURRENT << 4) | LED_27_CURRENT) #IR and Red Current to 27.1, 4 bit for IR, 4 bit for Red

        #Configuration for SPO2
        spo2_reg = self.i2c.read_byte_data(MAX30100_ADDR, SPO2_CONFIGURATION)
        self.i2c.write_byte_data(MAX30100_ADDR, SPO2_CONFIGURATION, spo2_reg & 0xFC | PULSE_WIDTH)
    
    def set_mode_spo2(self):
        self.i2c.write_byte_data(MAX30100_ADDR, MODE_CONFIGURATION, MODE_SPO2)
        
    def set_mode_hr(self):
        self.i2c.write_byte_data(MAX30100_ADDR, MODE_CONFIGURATION, MODE_HR)

    #Read IR and Red using MAX30100
    def update_values(self):
        readings = self.i2c.read_i2c_block_data(MAX30100_ADDR, FIFO_DATA_REGISTER, 4) #Read 4 blocks from FIFO DATA REGISTER
        self.current_ir = (readings[0] << 8) | readings[1] #Update the IR value to be read later in main.py
        self.current_red = (readings[2] << 8) | readings[3] #Update the Red value to be read later in main.py

'''
def main():
    mx30 = MAX30100()
    while True:
        mx30.update_values()
        print("IR: ", mx30.current_ir)
        print("Red: ", mx30.current_red)
        time.sleep(0.01)

if __name__ == "__main__" :
    main()
    
'''
