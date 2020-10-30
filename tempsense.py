# -*- coding: utf-8 -*-
import time
import datetime
import busio
import digitalio
import board
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
increment = 0
timer = 10
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)#setting up button for channel 5 on raspberrypi
GPIO.add_event_detect(5,GPIO.FALLING,callback=incrementer,bouncetime=250)
print("RunTime\tTemp Reading\tTemp")
starter=time.time()
def incrementer():
	if increment==2:
		increment=0
	else: increment+=1
	if increment==0: 
        timer=10
	if increment==1: 
        timer=5
	if increment==2: 
        timer=1

    fetch_slave()

def fetch_slave():
    RunTime= time.time()-starter
    # create an analog input channel on pin 0
    chan = AnalogIn(mcp, MCP.P0)
    temperature = ((((chan.value * 1000 * 3.3)/2**16)-500)/10)
    print(RunTime+"\t"+str(chan.value) +"\t"+ str(temperature) + "C")
    
    time.sleep(timer)
def main():
    while True:
        x = threading.Thread(target=fetch_slave, args=())
        x.start()
        x.join()           

if __name-- == "__main__"
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as e:
        print(e)
        GPIO.cleanup
    finally:
        GPIO.cleanup()
    