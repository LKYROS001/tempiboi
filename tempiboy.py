# -*- coding: utf-8 -*-
import spidev
import time
spi = spidev.SpiDev()
spi.open(0, 0)
def readadc(adcnum):
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    if adcnum > 7 or adcnum < 0:
        print("false reading")
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    print("true reading", adcout)
    return adcout
while True:
    value = readadc(0)
    volts = (value * 3.3) / 1024
    print(volts)
    temperature = volts / (10.0 / 1000)
    print ("%4d/1023 => %5.3f V => %4.1f °C" % (value, volts,
    temperature))
    time.sleep(0.5)