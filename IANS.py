import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import datetime
import time
import RPi.GPIO as GPIO
nbits = 16 
Vref = 3.3 #Volts 
Tc = 10 #mV/C 
T0 = 500
button1 = 5
timestep = [10,5,1]
chan = None
runtime = 0
option = 0
start = 0
thread = None
def ADCToCelcius(ADCcode):
    temp = (((ADCcode * Vref * 1000) / 2**nbits) - T0)/Tc 
    return temp

def get_time_thread():
    global chan, option, timestep, start, runtime, thread;
    runtime = time.time() - start;
    runtime=round(runtime) #Calculate runtime
    thread = threading.Timer(timestep[option], get_time_thread)
    thread.daemon = True #Clean up and close threads on program exit.
    thread.start() #start thread
    read(chan, runtime) #Thread displays ADC value every timer tick.
    
def btn_pressed(channel):
    global option, thread
    thread.cancel() #On button press, cancel the thread timer and restart it.
    option += 1
    if option > 2: #timestep has 3 options from 0 to 2.
        option = 0
    get_time_thread()
    
def setup():
    global start
    GPIO.setmode(GPIO.BCM)
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D5)
    mcp = MCP.MCP3008(spi, cs)
    chan = AnalogIn(mcp, MCP.P1)
    GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button1,GPIO.FALLING,callback=btn_pressed,bouncetime=300)
    print("Runtime\t\tTemp Reading\tTemp")
    start=time.time()
    return chan #object of analog input channel for ADC returned.
    
def read(chan, runtime):
    val = chan.value
    print(runtime, "\t\t", chan.value, '\t\t', str(round(ADCToCelcius(val),3)) + "\tC", sep = '')
    
def main():
    global chan #global variables used in the function
    chan = setup()
    get_time_thread() #Start timer and reading function
    while True: #loop infinitely so thread can run and print ADC values to display. Note: timer does printing so ADC is only read and printed to display each timestep.
        pass

if __name__ == "__main__": #If run as the main script, run main()
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup() #Cleanup GPIO initializations on exit.
    except Exception as e:
        print(e)
        GPIO.cleanup()
    finally:
        GPIO.cleanup()