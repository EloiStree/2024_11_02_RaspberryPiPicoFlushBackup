import time
from machine import Pin
from machine import UART
import sys
import utime

print("Hello World")

# 0; Set all pin to false 
# 1; Set all pin to true 
# d01; Set pin at index 1 to false
# d15; Set pin at index 5 to True
# d120; Set pin at index 20 to True
# d021; Set pin at index 21 to False
# d041; Will ignore as pin at index 41 is not registered
# ; or \n will end the serial message
# ' ' will split the message in several command
#Example: 0 d12 d120 d04;


#Blink: d015 d115 d015  ;
#Set direction down: d015;
#Set direction up: d115;
# d114 d015 d115 d015  ;
# d014 d015 d115 d015  ;
    

## Set the power of the remote control on at star
power_on_at_start=True
default_value=False

## Will trigger a while loop to run 8 9 10 11 pins in a loop
#debug_test=False
debug_test=False

usePrintlog=True

class GPIOPin:
    def __init__(self, pin_id, pin):
        self.m_pin_id = pin_id
        self.m_pin = pin

class DelayMessage:
    def __init__(self):
        self.m_timeReach=True
        self.m_command = "0123"
        self.m_timestamp = utime.ticks_ms()
        
    def set_command(self, command, millisecond):
        self.m_timeReach=False
        self.m_command = command
        self.m_timestamp = utime.ticks_ms() + int(millisecond)
        
    def set_command_at(self, command, timestamp):
        self.m_timeReach=False
        self.m_command = command
        self.m_timestamp = timestamp
        
    def set_as_used(self):
        self.m_timeReach=True
    
    def is_to_dealed_with(self):
        return self.m_timeReach==False
        
    def is_time_reach(self):
        return utime.ticks_ms() >= self.m_timestamp


delayIndex=0
maxIndex=40
delayArray = [
]
for i in range(0,maxIndex):
    delayArray.append(DelayMessage())


            

timestamp_ms = utime.ticks_ms()
print("Timestamp in milliseconds:", timestamp_ms)
    

## All the pin to use.
## Raspberry Pi Pico pin available
pins_id = [
     2, 3, 4, 5, 6,
     7, 8, 9,10,11,
    12,13,14,15,16,
    17,18,19,20,21,
    22,26,27,28
]
## All the pin objects of the RC car to control
pins_id_created= [
    
]

## All the pin objects of the RC car to control
pins_id_auto_created= [
    
]


def initiate_all_as_out():
    for pin in pins_id:
        pin = Pin(pin, Pin.OUT)
        pin.value(default_value)
        pins_id_created.append(pin)

def set_all_to(state):
    for pin in pins_id_created:
        pin.value( state)
        
def set_pin_to(index ,state):
    if index>-1 and index < len(pins_id_created) :
        pins_id_created[index].value( state)
        
def set_gpio_to(index ,state):
    for p in pins_id_auto_created:
        if p.m_pin_id == index:
            if usePrintlog:
                print(p)
            p.m_pin.value( state)
            
def add_delay_command(shortcut, msToAdd):
    for c in delayArray:
        if not c.is_to_dealed_with():
            c.set_command(shortcut, msToAdd)
            
def add_time_command(shortcut, timestamp):
    for c in delayArray:
        if not c.is_to_dealed_with():
            c.set_command_at(shortcut, timestamp)
            return
            
            
#def set_gpio_to(index ,state):
#    if index>-1 and index < len(pins_id_created) :
#        pins_id_created[index].value( state)
#        #pin.value( state? motorOn : motoroff)

def charToInt(c):
    if c=='1':
        return 1
    elif c=='2':
        return 2
    elif c=='3':
        return 3
    elif c=='4':
        return 4
    elif c=='5':
        return 5
    elif c=='6':
        return 6
    elif c=='7':
        return 7
    elif c=='8':
        return 8
    elif c=='9':
        return 9
    elif c=='0':
        return 0
    return -1


def set_pins_direction():
    for pin_num in range(0,41):
        try:
            pin = machine.Pin(pin_num)
            pin.init(mode=machine.Pin.OUT)
            if usePrintlog:
                print("Set pin {} direction to OUT".format(pin_num))
            pinLin = GPIOPin(pin_num, pin)
            pins_id_auto_created.append(pinLin)
        except:
            if usePrintlog:
                print("Ignoring pin {} (not usable)".format(pin_num))

def uartToAction(message):
    if usePrintlog:
        print("|"+message+"|")
    tokens = message.split(' ')
    tstart = utime.ticks_ms()
    msToAdd=0
    
    for shortcut in tokens:
        shortcut = shortcut.strip().lower()
        if usePrintlog:
            print("#"+shortcut+"#")
           
        if shortcut.endswith('>'):
            intValue = int(shortcut[:-1])
            msToAdd+= intValue
            print("MS "+ str(msToAdd))
            
        elif shortcut.endswith('|'):
            intValue = int(shortcut[:-1])
            msToAdd = intValue
            print("MS AT "+ str(msToAdd))
            
        else:
            
            if msToAdd>0:
                add_time_command(shortcut, int(tstart+msToAdd))
                if usePrintlog:
                    print("Delay "+ shortcut +" MS "+ str(msToAdd)+"  T"+ str(tstart+msToAdd))
                
            if msToAdd <= 0:
                if shortcut == "1":
                    set_all_to(True)
                    
                    
                if shortcut == "0":
                    set_all_to(False)
                    
                if shortcut == "test":
                    full_test()
                    
                    
                length =len(shortcut)
                if length > 0:
                    isDigital = shortcut[0]=='d'
                    isGpio = shortcut[0]=='g'
                    if length > 2 and ( isDigital or isGpio):
                        isOn = shortcut[1] != '0'
                        if length==3:
                            c = charToInt(shortcut[2])
                            if c > -1:
                                if usePrintlog:
                                    print("D3 "+str(c)+" " + str(isOn))
                                if isDigital:
                                    set_pin_to(c,isOn) 
                                if isGpio:
                                    set_gpio_to(c,isOn)                    
                        elif length==4:
                            c0 = charToInt(shortcut[2])
                            c1 = charToInt(shortcut[3])
                            if c0 > -1 and c1 > -1 : 
                                index= c0 * 10  + c1                
                                if usePrintlog:
                                    print("4D "+str(c0)+" "+str(c1)+" " + str(isOn)+" -GPIO "+str(pins_id[index]))
                                if isDigital:
                                    set_pin_to(index,isOn) 
                                if isGpio:
                                    set_gpio_to(index,isOn) 
                                

print("Hello World")
print("sys.implementation:{}".format(sys.implementation))
print("sys.version:{}".format(sys.version))

## Set all the pin of the board as out.
set_pins_direction()
## Set all the pin given in the script
initiate_all_as_out()

if default_value:
    set_all_to(power_on_at_start)
    
## UART is define after the pin full override to be able to set as read. 
uart = machine.UART(0, 9600)
uart.init(9600, bits=8, parity=None, stop=1)




def blink_all():
    time.sleep(1)
    set_all_to(False)
    time.sleep(1)
    set_all_to(True)
    time.sleep(1)
    set_all_to(False)
    time.sleep(1)
    
def step_blink():
    for pin in pins_id_created:
        pin.value(True)
        time.sleep(0.1)
        pin.value(False)
        time.sleep(0.1)
        
def line_blink():
    for pin in pins_id_created:
        pin.value(True)
        time.sleep(0.1)
    for pin in pins_id_created:
        pin.value(False)
        time.sleep(0.1)


def full_test():
    blink_all()
    line_blink()
    step_blink()

if debug_test:
    while True:
        
        for pin in pins_id_created:
            pin.value(True)
            time.sleep(0.1)
        for pin in pins_id_created:
            pin.value(False)
            time.sleep(0.1)

delayArray[0].set_command("0 200> 1 5000| 0 200> 1 500> 0 200> 1 200> D115 2000> test",2000)

"""
delayArray[0].set_command("D011",2000)
delayArray[1].set_command("D111",3000)
delayArray[2].set_command("D011",4000)
delayArray[3].set_command("D111",6000)
delayArray[4].set_command("D112",9000)
delayArray[5].set_command("0",10000)
delayArray[6].set_command("1",12000)
delayArray[7].set_command("0",15000)
delayArray[8].set_command("1",17000)
delayArray[9].set_command("0",21000)
"""


line = b''  # Initialize an empty line buffer
data = ' '

while True:
    if uart.any():
        data = uart.read(1)  # Read one byte at a time        if data == b'\n':  # Check for newline character
        if  data == b'\n' or data == b';':
            line = line.decode('utf-8').strip().lower()  # Decode the received line
            uartToAction(line)
            line = b''  # Reset the line buffer
        else:
            line += data  # Append the received byte to the line buffer
            

    for dCmd in delayArray:
        if dCmd.is_to_dealed_with():
            if dCmd.is_time_reach():
                dCmd.set_as_used()
                uartToAction(dCmd.m_command)
                print("Exe|"+dCmd.m_command+"|"+str(utime.ticks_ms())  +" - "+str(dCmd.m_timestamp) )
    

