# -*- coding: utf-8 -*-
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

while True:
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)


    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 0
    chan = AnalogIn(mcp, MCP.P0)
    temperature = chan.voltage / (10.0 / 1000)
    print("Raw ADC Value: ", chan.value)
    print("ADC Voltage: " + str(chan.voltage) + "V")
    print("Temp: " + str(temperature) + "C")
    time.sleep(0.5)
