# -*- coding: utf-8 -*-
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)

while true:
    x = threading.Thread(target=fetch_slave, args=())
    x.start()
    x.join()
def fetch_slave():
    # create an analog input channel on pin 0
    chan = AnalogIn(mcp, MCP.P0)
    # create an analog input channel on pin 1
    han = AnalogIn(mcp, MCP.P1)
    temperature = (chan.voltage * 100)-273
    temp2 = (han.voltage * 100)-273
   # print("Raw ADC Value: ", chan.value)
    print("**************************************************************************")
    print("First ADC Voltage: " + str(chan.voltage) + "V")
    print("First Temp: " + str(temperature) + "C")
    print("")
    print("Second ADC Voltage: " + str(han.voltage) + "V")
    print("Second Temp: " + str(temp2) + "C")
    print("**************************************************************************")
    print("")
    time.sleep(5)
