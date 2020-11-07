# -*- coding: utf-8 -*-
import time
import datetime
import busio
import digitalio
import board
import random
import threading
import os
import sys

import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from datetime import datetime
import ES2EEPROMUtils
from array import *
from time import mktime

btn_increment = 23
btn_log = 24
eeprom = ES2EEPROMUtils.ES2EEPROM() 

logFlag=True
spi=None
mcp=None
cs=None

counters=[10,5,1]
increment = 0
timer = 10

def setup():

    global btn_increment
    global btn_log
    global cs,mcp,spi

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


    #button setup
    GPIO.setup(btn_increment,GPIO.IN,pull_up_down=GPIO.PUD_UP)#setting up button for channel 16 on raspberrypi
    GPIO.setup(btn_log,GPIO.IN,pull_up_down=GPIO.PUD_UP)#setting up button for channel 18 on raspberrypi

    GPIO.add_event_detect(btn_increment,GPIO.FALLING,callback=incrementer,bouncetime=1000)
    GPIO.add_event_detect(btn_log,GPIO.FALLING,callback=logging,bouncetime=1000) 


    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D5)
    mcp = MCP.MCP3008(spi, cs)
    pass



def fetch_scores():

    #gets the top 3 results and converts them to a string output
    datalog = ''
    for x in range(1,21):
        name = eeprom.read_block(x,4)
        #score_count[x-1] =  name
        datalog += name+" "
     
    return datalog


def save_data(stamp, run,temp,buz):
   
    scores = [0]*20
    for x in range(1,21):
        name = eeprom.read_block(x,4)
        scores[x-1] =  name
    #add new entry to scores
    data = [stamp,run,100,buz]
    scores.insert(0,data)
    print(scores)
    i = 1
    #writes scores back to eeprom
    for x in scores:
        eeprom.write_block(i,x)
        i+=1
    pass

def logging():
    global logFlag
    logFlag = not (logFlag)
    pass

def incrementer(num):
    global increment,timer,counters
    increment+=1
    if increment > 2:
        increment=0
    timer = counters[increment]
    fetch_slave()

def fetch_slave():
    global starter,mcp,increment,timer,counters
    time.sleep(timer)
    RunTime= time.time()-starter
    # create an analog input channel on pin 1
    chan = AnalogIn(mcp, MCP.P1)
    temperature = ((((chan.value * 1000 * 3.3)/2**16)-500)/10)
    t = time.localtime()
    print(time.strftime("%H:%M:%S",t),"\t\t",round(RunTime,0),"\t\t","%.3f" % chan.value ,"\t\t", "%.3f" % temperature , "C")

    #preparing data for eeprom
    timestamp =int(mktime(t))
    #dt = datetime.fromtimestamp(mktime(t))
    RunTime =int(round(RunTime,0))
    temperature = int(round(temperature,1)*10)    #need a float as an int, will take 1 decimal place, times by 10 to get keep decimal when converting to int
    save_data(timestamp,RunTime,temperature,0)


def menu():
    global logFlag
    global starter
   
    starter=time.time()
    while True:
        print("hello to minitoring system")
        option = input('press 1 to monitor for 20 seconds or press 2 to view eeprom data\n')
        if option == "1":
            os.system('clear')
            print("Time\t\tSys Timer\t\tTemp\t\tBuzzer")
            i=0
            while logFlag:
                x = threading.Thread(target=fetch_slave, args=())
                x.start()
                x.join()
                i+=1
                if i==2:
                    logFlag=False
        else:
            print(fetch_scores)




if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        eeprom.clear(4096)
        menu()
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()