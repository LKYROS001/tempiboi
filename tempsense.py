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



def incrementer():
    increment+=1
    if increment > 2:
        increment=0
    timer = counters[increment]
    fetch_slave()

def fetch_slave():
    RunTime= time.time()-starter
    # create an analog input channel on pin 1
    chan = AnalogIn(mcp, MCP.P1)
    temperature = ((((chan.value * 1000 * 3.3)/2**16)-500)/10)
    print(RunTime,"\t","%.3f" % chan.value ,"\t", "%.3f" % temperature , "C")
    
    time.sleep(timer)
def main():
    global starter,mcp,increment,timer,counters
    GPIO.setmode(GPIO.BCM)
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    counters=[10,5,1]
    increment = 0
    timer = 10
    GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP)#setting up button for channel 5 on raspberrypi
    GPIO.add_event_detect(6,GPIO.FALLING,callback=incrementer,bouncetime=300)
    #GPIO.setup(8,GPIO.OUT)
    print("RunTime\tTemp Reading\tTemp")
    starter=time.time()
    while True:
        #fetch_slave()
        x = threading.Thread(target=fetch_slave, args=())
        x.start()
        x.join()           

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as e:
        print(e)
        GPIO.cleanup
    finally:
        GPIO.cleanup()
    