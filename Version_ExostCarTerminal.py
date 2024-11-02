# Previous project on the topic:
# https://github.com/EloiStree/2023_06_28_RasperryPiPicoToRemoteControlRCExostCar/
# https://github.com/EloiStree/2023_06_29_MicroPythonUART2PinOnOff
#98:D3:21:F7:3B:8D
import time
from machine import Pin
from machine import UART
import sys
import utime

#startcommand="A1B1C1D1 E1F1G1H1 I1J1K0L0 M0N0O0P0 Q0R0S0T0 U0V0W0X0 "
startcommand="G3H3I3J3 K3L3M3N3 O3P3 Q2R2S2T2 U2V2W2X2 "

baudrate1=9600 #Default
#baudrate1=38400 #Fast Bluetooth
#baudrate1=115200 #Fast USB TTL

## Set the power of the remote control on at star
power_on_at_start=True
default_value=False

## Will trigger a while loop to run 8 9 10 11 pins in a loop
#debug_test=False
debug_test=False
debug_full_test=False
debug_inverse_test=True
inversetestspeed=0.1

usePrintlog=False
# If you want to have Bluetooth and TTL usb cable to controle the device.
useTwoTXRX=True


class GPIOPin:
    def __init__(self, pin_id, pin):
        self.m_pin_id = pin_id
        self.m_pin = pin

## All the pin to use.
## Raspberry Pi Pico pin available
if useTwoTXRX==False:
    pins_id = [
         2, 3, 4, 5, 6,
         7, 8, 9,10,11,
        12,13,14,15,16,
        17,18,19,20,21,
        22,26,27,28
    ]
else :
    ## If using two TXRX 0 and 1
    pins_id = [
        2, 3, 6,
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
        
def inverse_pin_to(index ):
    if index>-1 and index < len(pins_id_created) :
        pins_id_created[index].value( not pins_id_created[index].value)
        
def set_gpio_to(index ,state):
    for p in pins_id_auto_created:
        if p.m_pin_id == index:
            if usePrintlog:
                print(p)
            p.m_pin.value( state)
                   

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

def inverse_step_blink():
    for pin in pins_id_created:
        pin.value(not pin.value())
        time.sleep(inversetestspeed)
        pin.value(not pin.value())
        time.sleep(inversetestspeed)
        
def line_blink():
    for pin in pins_id_created:
        pin.value(True)
        time.sleep(0.1)
    for pin in pins_id_created:
        pin.value(False)
        time.sleep(0.1)


def full_test():
    step_blink()
    blink_all()
    line_blink()



#command_dict = {
#    'a': set_all_to,
#    'b': set_all_to,
#    'c': step_blink,
#    'd': line_blink,
#    'e': full_test,
#    'f': print("Hey"),
#}
    #if message in command_dict:
    #    command_dict[message]()
    #else:
    #    print("Invalid command"+ str(message));
    
    
def split_string_to_utf8_chars(input_string):
    utf8_chars = []
    i = 0
    while i < len(input_string):
        char = input_string[i]
        if ord(char) < 128:
            utf8_chars.append(char)
            i += 1
        else:
            # Handle multi-byte UTF-8 characters
            char_bytes = [char]
            i += 1
            while i < len(input_string) and (ord(input_string[i]) & 0xC0) == 0x80:
                char_bytes.append(input_string[i])
                i += 1
            utf8_chars.append(''.join(char_bytes))
    return utf8_chars


    
def uartToAction(c0, c1):                               
    timestamp_ms = utime.ticks_ms()
    if usePrintlog:
        print("Timestamp in milliseconds:", timestamp_ms)
    # 1357 2468
    if c1=='1':
        if c0=='!' :
            set_all_to(True)
        elif c0=='"' :
            print("Add Code")
        elif c0=='#' :
            print("Add Code")
        elif c0=='$' :
            print("Add Code")
        elif c0=='%' :
            print("Add Code")
        elif c0=='&' :
            print("Add Code")
        elif c0=='\'' :
            print("Add Code")
        elif c0=='(' :
            print("Add Code")
        elif c0==')' :
            print("Add Code")
        elif c0=='*' :
            print("Add Code")
        elif c0=='+' :
            print("Add Code")
        elif c0==',' :
            print("Add Code")
        elif c0=='-' :
            print("Add Code")
        elif c0=='.' :
            print("Add Code")
        elif c0=='/' :
            print("Add Code")
        elif c0==':' :
            print("Add Code")
        elif c0==';' :
            print("Add Code")
        elif c0=='<' :
            print("Add Code")
        elif c0=='=' :
            print("Add Code")
        elif c0=='>' :
            print("Add Code")
        elif c0=='?' :
            print("Add Code")
        elif c0=='@' :
            print("Add Code")
        elif c0=='A' :
            set_pin_to(0,True) 
        elif c0=='B' :
            set_pin_to(1,True) 
        elif c0=='C' :
            set_pin_to(2,True) 
        elif c0=='D' :
            set_pin_to(3,True) 
        elif c0=='E' :
            set_pin_to(4,True) 
        elif c0=='F' :
            set_pin_to(5,True) 
        elif c0=='G' :
            set_pin_to(6,True) 
        elif c0=='H' :
            set_pin_to(7,True) 
        elif c0=='I' :
            set_pin_to(8,True) 
        elif c0=='J' :
            set_pin_to(9,True) 
        elif c0=='K' :
            set_pin_to(10,True) 
        elif c0=='L' :
            set_pin_to(11,True) 
        elif c0=='M' :
            set_pin_to(12,True) 
        elif c0=='N' :
            set_pin_to(13,True) 
        elif c0=='O' :
            set_pin_to(14,True) 
        elif c0=='P' :
            set_pin_to(15,True) 
        elif c0=='Q' :
            set_pin_to(16,True) 
        elif c0=='R' :
            set_pin_to(17,True) 
        elif c0=='S' :
            set_pin_to(18,True) 
        elif c0=='T' :
            set_pin_to(19,True) 
        elif c0=='U' :
            set_pin_to(20,True) 
        elif c0=='V' :
            set_pin_to(21,True) 
        elif c0=='W' :
            set_pin_to(22,True) 
        elif c0=='X' :
            set_pin_to(23,True) 
        elif c0=='Y' :
            set_pin_to(24,True) 
        elif c0=='Z' :
            set_pin_to(25,True) 
        elif c0=='[' :
            print("Add Code")
        elif c0=='\\' :
            print("Add Code")
        elif c0==']' :
            print("Add Code")
        elif c0=='^' :
            print("Add Code")
        elif c0=='_' :
            print("Add Code")
        elif c0=='`' :
            print("Add Code")
        elif c0=='a' :
            set_pin_to(26,True) 
        elif c0=='b' :
            set_pin_to(27,True) 
        elif c0=='c' :
            set_pin_to(28,True) 
        elif c0=='d' :
            set_pin_to(29,True) 
        elif c0=='e' :
            set_pin_to(30,True) 
        elif c0=='f' :
            set_pin_to(31,True) 
        elif c0=='g' :
            set_pin_to(32,True) 
        elif c0=='h' :
            set_pin_to(33,True) 
        elif c0=='i' :
            set_pin_to(34,True) 
        elif c0=='j' :
            set_pin_to(35,True) 
        elif c0=='k' :
            set_pin_to(36,True) 
        elif c0=='l' :
            set_pin_to(37,True) 
        elif c0=='m' :
            set_pin_to(38,True) 
        elif c0=='n' :
            set_pin_to(39,True) 
        elif c0=='o' :
            set_pin_to(40,True) 
        elif c0=='p' :
            set_pin_to(41,True) 
        elif c0=='q' :
            set_pin_to(42,True) 
        elif c0=='r' :
            set_pin_to(43,True) 
        elif c0=='s' :
            set_pin_to(44,True) 
        elif c0=='t' :
            set_pin_to(45,True) 
        elif c0=='u' :
            set_pin_to(46,True) 
        elif c0=='v' :
            set_pin_to(47,True) 
        elif c0=='w' :
            set_pin_to(48,True) 
        elif c0=='x' :
            set_pin_to(49,True) 
        elif c0=='y' :
            set_pin_to(50,True) 
        elif c0=='z' :
            set_pin_to(51,True) 
        elif c0=='{' :
            print("Add Code")
        elif c0=='|' :
            print("Add Code")
        elif c0=='}' :
            print("Add Code")
        elif c0=='~' :
            print("Add Code")


    elif c1=='0':
        if c0=='!' :
            set_all_to(False)
        elif c0=='"' :
            print("Add Code")
        elif c0=='#' :
            print("Add Code")
        elif c0=='$' :
            print("Add Code")
        elif c0=='%' :
            print("Add Code")
        elif c0=='&' :
            print("Add Code")
        elif c0=='\'' :
            print("Add Code")
        elif c0=='(' :
            print("Add Code")
        elif c0==')' :
            print("Add Code")
        elif c0=='*' :
            print("Add Code")
        elif c0=='+' :
            print("Add Code")
        elif c0==',' :
            print("Add Code")
        elif c0=='-' :
            print("Add Code")
        elif c0=='.' :
            print("Add Code")
        elif c0=='/' :
            print("Add Code")
        elif c0==':' :
            print("Add Code")
        elif c0==';' :
            print("Add Code")
        elif c0=='<' :
            print("Add Code")
        elif c0=='=' :
            print("Add Code")
        elif c0=='>' :
            print("Add Code")
        elif c0=='?' :
            print("Add Code")
        elif c0=='@' :
            print("Add Code")
        elif c0=='A' :
            set_pin_to(0,False) 
        elif c0=='B' :
            set_pin_to(1,False) 
        elif c0=='C' :
            set_pin_to(2,False) 
        elif c0=='D' :
            set_pin_to(3,False) 
        elif c0=='E' :
            set_pin_to(4,False) 
        elif c0=='F' :
            set_pin_to(5,False) 
        elif c0=='G' :
            set_pin_to(6,False) 
        elif c0=='H' :
            set_pin_to(7,False) 
        elif c0=='I' :
            set_pin_to(8,False) 
        elif c0=='J' :
            set_pin_to(9,False) 
        elif c0=='K' :
            set_pin_to(10,False) 
        elif c0=='L' :
            set_pin_to(11,False) 
        elif c0=='M' :
            set_pin_to(12,False) 
        elif c0=='N' :
            set_pin_to(13,False) 
        elif c0=='O' :
            set_pin_to(14,False) 
        elif c0=='P' :
            set_pin_to(15,False) 
        elif c0=='Q' :
            set_pin_to(16,False) 
        elif c0=='R' :
            set_pin_to(17,False) 
        elif c0=='S' :
            set_pin_to(18,False) 
        elif c0=='T' :
            set_pin_to(19,False) 
        elif c0=='U' :
            set_pin_to(20,False) 
        elif c0=='V' :
            set_pin_to(21,False) 
        elif c0=='W' :
            set_pin_to(22,False) 
        elif c0=='X' :
            set_pin_to(23,False) 
        elif c0=='Y' :
            set_pin_to(24,False) 
        elif c0=='Z' :
            set_pin_to(25,False) 
        elif c0=='[' :
            print("Add Code")
        elif c0=='\\' :
            print("Add Code")
        elif c0==']' :
            print("Add Code")
        elif c0=='^' :
            print("Add Code")
        elif c0=='_' :
            print("Add Code")
        elif c0=='`' :
            print("Add Code")
        elif c0=='a' :
            set_pin_to(26,False) 
        elif c0=='b' :
            set_pin_to(27,False) 
        elif c0=='c' :
            set_pin_to(28,False) 
        elif c0=='d' :
            set_pin_to(29,False) 
        elif c0=='e' :
            set_pin_to(30,False) 
        elif c0=='f' :
            set_pin_to(31,False) 
        elif c0=='g' :
            set_pin_to(32,False) 
        elif c0=='h' :
            set_pin_to(33,False) 
        elif c0=='i' :
            set_pin_to(34,False) 
        elif c0=='j' :
            set_pin_to(35,False) 
        elif c0=='k' :
            set_pin_to(36,False) 
        elif c0=='l' :
            set_pin_to(37,False) 
        elif c0=='m' :
            set_pin_to(38,False) 
        elif c0=='n' :
            set_pin_to(39,False) 
        elif c0=='o' :
            set_pin_to(40,False) 
        elif c0=='p' :
            set_pin_to(41,False) 
        elif c0=='q' :
            set_pin_to(42,False) 
        elif c0=='r' :
            set_pin_to(43,False) 
        elif c0=='s' :
            set_pin_to(44,False) 
        elif c0=='t' :
            set_pin_to(45,False) 
        elif c0=='u' :
            set_pin_to(46,False) 
        elif c0=='v' :
            set_pin_to(47,False) 
        elif c0=='w' :
            set_pin_to(48,False) 
        elif c0=='x' :
            set_pin_to(49,False) 
        elif c0=='y' :
            set_pin_to(50,False) 
        elif c0=='z' :
            set_pin_to(51,False) 
        elif c0=='{' :
            print("Add Code")
        elif c0=='|' :
            print("Add Code")
        elif c0=='}' :
            print("Add Code")
        elif c0=='~' :
            print("Add Code")

    elif c1=='3':
        if c0=='!' :
            print("Add Code")
        elif c0=='"' :
            print("Add Code")
        elif c0=='#' :
            print("Add Code")
        elif c0=='$' :
            print("Add Code")
        elif c0=='%' :
            print("Add Code")
        elif c0=='&' :
            print("Add Code")
        elif c0=='\'' :
            print("Add Code")
        elif c0=='(' :
            print("Add Code")
        elif c0==')' :
            print("Add Code")
        elif c0=='*' :
            print("Add Code")
        elif c0=='+' :
            print("Add Code")
        elif c0==',' :
            print("Add Code")
        elif c0=='-' :
            print("Add Code")
        elif c0=='.' :
            print("Add Code")
        elif c0=='/' :
            print("Add Code")
        elif c0==':' :
            print("Add Code")
        elif c0==';' :
            print("Add Code")
        elif c0=='<' :
            print("Add Code")
        elif c0=='=' :
            print("Add Code")
        elif c0=='>' :
            print("Add Code")
        elif c0=='?' :
            print("Add Code")
        elif c0=='@' :
            print("Add Code")
        elif c0=='A' :
            set_gpio_to(0,True) 
        elif c0=='B' :
            set_gpio_to(1,True) 
        elif c0=='C' :
            set_gpio_to(2,True) 
        elif c0=='D' :
            set_gpio_to(3,True) 
        elif c0=='E' :
            set_gpio_to(4,True) 
        elif c0=='F' :
            set_gpio_to(5,True) 
        elif c0=='G' :
            set_gpio_to(6,True) 
        elif c0=='H' :
            set_gpio_to(7,True) 
        elif c0=='I' :
            set_gpio_to(8,True) 
        elif c0=='J' :
            set_gpio_to(9,True) 
        elif c0=='K' :
            set_gpio_to(10,True) 
        elif c0=='L' :
            set_gpio_to(11,True) 
        elif c0=='M' :
            set_gpio_to(12,True) 
        elif c0=='N' :
            set_gpio_to(13,True) 
        elif c0=='O' :
            set_gpio_to(14,True) 
        elif c0=='P' :
            set_gpio_to(15,True) 
        elif c0=='Q' :
            set_gpio_to(16,True) 
        elif c0=='R' :
            set_gpio_to(17,True) 
        elif c0=='S' :
            set_gpio_to(18,True) 
        elif c0=='T' :
            set_gpio_to(19,True) 
        elif c0=='U' :
            set_gpio_to(20,True) 
        elif c0=='V' :
            set_gpio_to(21,True) 
        elif c0=='W' :
            set_gpio_to(22,True) 
        elif c0=='X' :
            set_gpio_to(23,True) 
        elif c0=='Y' :
            set_gpio_to(24,True) 
        elif c0=='Z' :
            set_gpio_to(25,True) 
        elif c0=='[' :
            print("Add Code")
        elif c0=='\\' :
            print("Add Code")
        elif c0==']' :
            print("Add Code")
        elif c0=='^' :
            print("Add Code")
        elif c0=='_' :
            print("Add Code")
        elif c0=='`' :
            print("Add Code")
        elif c0=='a' :
            set_gpio_to(26,True) 
        elif c0=='b' :
            set_gpio_to(27,True) 
        elif c0=='c' :
            set_gpio_to(28,True) 
        elif c0=='d' :
            set_gpio_to(29,True) 
        elif c0=='e' :
            set_gpio_to(30,True) 
        elif c0=='f' :
            set_gpio_to(31,True) 
        elif c0=='g' :
            set_gpio_to(32,True) 
        elif c0=='h' :
            set_gpio_to(33,True) 
        elif c0=='i' :
            set_gpio_to(34,True) 
        elif c0=='j' :
            set_gpio_to(35,True) 
        elif c0=='k' :
            set_gpio_to(36,True) 
        elif c0=='l' :
            set_gpio_to(37,True) 
        elif c0=='m' :
            set_gpio_to(38,True) 
        elif c0=='n' :
            set_gpio_to(39,True) 
        elif c0=='o' :
            set_gpio_to(40,True) 
        elif c0=='p' :
            set_gpio_to(41,True) 
        elif c0=='q' :
            set_gpio_to(42,True) 
        elif c0=='r' :
            set_gpio_to(43,True) 
        elif c0=='s' :
            set_gpio_to(44,True) 
        elif c0=='t' :
            set_gpio_to(45,True) 
        elif c0=='u' :
            set_gpio_to(46,True) 
        elif c0=='v' :
            set_gpio_to(47,True) 
        elif c0=='w' :
            set_gpio_to(48,True) 
        elif c0=='x' :
            set_gpio_to(49,True) 
        elif c0=='y' :
            set_gpio_to(50,True) 
        elif c0=='z' :
            set_gpio_to(51,True) 
        elif c0=='{' :
            print("Add Code")
        elif c0=='|' :
            print("Add Code")
        elif c0=='}' :
            print("Add Code")
        elif c0=='~' :
            print("Add Code")


    elif c1=='2':
        if c0=='!' :
            print("Add Code")
        elif c0=='"' :
            print("Add Code")
        elif c0=='#' :
            print("Add Code")
        elif c0=='$' :
            print("Add Code")
        elif c0=='%' :
            print("Add Code")
        elif c0=='&' :
            print("Add Code")
        elif c0=='\'' :
            print("Add Code")
        elif c0=='(' :
            print("Add Code")
        elif c0==')' :
            print("Add Code")
        elif c0=='*' :
            print("Add Code")
        elif c0=='+' :
            print("Add Code")
        elif c0==',' :
            print("Add Code")
        elif c0=='-' :
            print("Add Code")
        elif c0=='.' :
            print("Add Code")
        elif c0=='/' :
            print("Add Code")
        elif c0==':' :
            print("Add Code")
        elif c0==';' :
            print("Add Code")
        elif c0=='<' :
            print("Add Code")
        elif c0=='=' :
            print("Add Code")
        elif c0=='>' :
            print("Add Code")
        elif c0=='?' :
            print("Add Code")
        elif c0=='@' :
            print("Add Code")
        elif c0=='A' :
            set_gpio_to(0,False) 
        elif c0=='B' :
            set_gpio_to(1,False) 
        elif c0=='C' :
            set_gpio_to(2,False) 
        elif c0=='D' :
            set_gpio_to(3,False) 
        elif c0=='E' :
            set_gpio_to(4,False) 
        elif c0=='F' :
            set_gpio_to(5,False) 
        elif c0=='G' :
            set_gpio_to(6,False) 
        elif c0=='H' :
            set_gpio_to(7,False) 
        elif c0=='I' :
            set_gpio_to(8,False) 
        elif c0=='J' :
            set_gpio_to(9,False) 
        elif c0=='K' :
            set_gpio_to(10,False) 
        elif c0=='L' :
            set_gpio_to(11,False) 
        elif c0=='M' :
            set_gpio_to(12,False) 
        elif c0=='N' :
            set_gpio_to(13,False) 
        elif c0=='O' :
            set_gpio_to(14,False) 
        elif c0=='P' :
            set_gpio_to(15,False) 
        elif c0=='Q' :
            set_gpio_to(16,False) 
        elif c0=='R' :
            set_gpio_to(17,False) 
        elif c0=='S' :
            set_gpio_to(18,False) 
        elif c0=='T' :
            set_gpio_to(19,False) 
        elif c0=='U' :
            set_gpio_to(20,False) 
        elif c0=='V' :
            set_gpio_to(21,False) 
        elif c0=='W' :
            set_gpio_to(22,False) 
        elif c0=='X' :
            set_gpio_to(23,False) 
        elif c0=='Y' :
            set_gpio_to(24,False) 
        elif c0=='Z' :
            set_gpio_to(25,False) 
        elif c0=='[' :
            print("Add Code")
        elif c0=='\\' :
            print("Add Code")
        elif c0==']' :
            print("Add Code")
        elif c0=='^' :
            print("Add Code")
        elif c0=='_' :
            print("Add Code")
        elif c0=='`' :
            print("Add Code")
        elif c0=='a' :
            set_gpio_to(26,False) 
        elif c0=='b' :
            set_gpio_to(27,False) 
        elif c0=='c' :
            set_gpio_to(28,False) 
        elif c0=='d' :
            set_gpio_to(29,False) 
        elif c0=='e' :
            set_gpio_to(30,False) 
        elif c0=='f' :
            set_gpio_to(31,False) 
        elif c0=='g' :
            set_gpio_to(32,False) 
        elif c0=='h' :
            set_gpio_to(33,False) 
        elif c0=='i' :
            set_gpio_to(34,False) 
        elif c0=='j' :
            set_gpio_to(35,False) 
        elif c0=='k' :
            set_gpio_to(36,False) 
        elif c0=='l' :
            set_gpio_to(37,False) 
        elif c0=='m' :
            set_gpio_to(38,False) 
        elif c0=='n' :
            set_gpio_to(39,False) 
        elif c0=='o' :
            set_gpio_to(40,False) 
        elif c0=='p' :
            set_gpio_to(41,False) 
        elif c0=='q' :
            set_gpio_to(42,False) 
        elif c0=='r' :
            set_gpio_to(43,False) 
        elif c0=='s' :
            set_gpio_to(44,False) 
        elif c0=='t' :
            set_gpio_to(45,False) 
        elif c0=='u' :
            set_gpio_to(46,False) 
        elif c0=='v' :
            set_gpio_to(47,False) 
        elif c0=='w' :
            set_gpio_to(48,False) 
        elif c0=='x' :
            set_gpio_to(49,False) 
        elif c0=='y' :
            set_gpio_to(50,False) 
        elif c0=='z' :
            set_gpio_to(51,False) 
        elif c0=='{' :
            print("Add Code")
        elif c0=='|' :
            print("Add Code")
        elif c0=='}' :
            print("Add Code")
        elif c0=='~' :
            print("Add Code")
     
        



print("Hello World")
print("sys.implementation:{}".format(sys.implementation))
print("sys.version:{}".format(sys.version))

## Set all the pin of the board as out.
set_pins_direction()
## Set all the pin given in the script
initiate_all_as_out()

if default_value:
    set_all_to(power_on_at_start)
    
## UART 0 is define after the pin full override to be able to set as read. 
uart = machine.UART(0, baudrate1)
uart.init(baudrate1, bits=8, parity=None, stop=1,tx=Pin(0), rx=Pin(1))


if useTwoTXRX==True:
    ##UART 1 if you need TTL and Bluetooth
    uartble = machine.UART(1,  baudrate=9600,tx=Pin(4), rx=Pin(5))
    uartble.init(9600, bits=8, parity=None, stop=1)


if debug_test:
    while True:
        for pin in pins_id_created:
            pin.value(True)
            time.sleep(0.7)
        for pin in pins_id_created:
            pin.value(False)
            time.sleep(0.7)


if debug_full_test:
    full_test()
    
line = b''  # Initialize an empty line buffer
data = ' '
charUtf8=""
charUtf8Int=0


#for code_point in range(256):
#    char = chr(code_point)
#    print(f"Code Point: {code_point}, Character: {char}")

c=' '
charOne=' '
charTwo=' '
data2 = ' '

c2=' '
charOne2=' '
charTwo2=' '

c3=' '
charOne3=' '
charTwo3=' '
#A1B1C1D1E1F1G1H1I1J1K1L1M1N1O1P1Q1R1S1T1U1V1W1X1
#A0B0C0D0E0F0G0H0I0J0K0L0M0N0O0P0Q0R0S0T0U0V0W0X0
#A1B1C1D1E1F1G1H1I1J1K1L1M1N1O1P1Q1R1S1T1U1V1W1X1 A0B0C0D0E0F0G0H0I0J0K0L0M0N0O0P0Q0R0S0T0U0V0W0X0
#A2B2C2D2E2F2G2H2I2J2K2L2M2N2O2P2Q2R2S2T2U2V2W2X2Y2Z2a2b2
#A3B3C3D3E3F3G3H3I3J3K3L3M3N3O3P3Q3R3S3T3U3V3W3X3Y3Z3a3b3

def uartToActionString(message):
    for	c3 in message:
        if c3=='0' or c3=='1'  or  c3=='2'  or  c3=='3'  or  c3=='4'  or  c3=='5'  or  c3=='6'  or  c3=='7'  or  c3=='8'  or  c3=='9' :
            charTwo3= c3
            uartToAction(charOne3,charTwo3)
        else :
            charOne3 = c3
        if usePrintlog:
            print(f"Code Point: {c3} {charOne3}  {charTwo3}")
    
    
uartToActionString(startcommand)
if debug_inverse_test:
    inverse_step_blink()
while True:
    if uart.any():
        data = uart.read(1)
        try:
            c = data.decode('utf-8')
            print(c)
            if c=='0' or c=='1'  or  c=='2'  or  c=='3'  or  c=='4'  or  c=='5'  or  c=='6'  or  c=='7'  or  c=='8'  or  c=='9' :
                charTwo= c
                uartToAction(charOne,charTwo)
            else :
                charOne = c
            if usePrintlog:
                print(f"Code Point: {data} {charOne}  {charTwo}")
        except Exception as e:
            # Handling any other exceptions
            print("An error occurred:", e)
            
    if useTwoTXRX==True:
        # IF YOU WANT SECOND BLE ART        
        if uartble.any():
            data2 = uartble.read(1)
            try:
                c2 = data2.decode('utf-8')
                print(c2)
                if c2=='0' or c2=='1'  or  c2=='2'  or  c2=='3'  or  c2=='4'  or  c2=='5'  or  c2=='6'  or  c2=='7'  or  c2=='8'  or  c2=='9' :
                   charTwo2= c2
                   uartToAction(charOne2,charTwo2)
                else :
                    charOne2 = c2
                if usePrintlog:
                    print(f"Code Point: {data2} {charOne2}  {charTwo2}")
            except Exception as e:
                # Handling any other exceptions
                print("An error occurred:", e)
       
            
 
