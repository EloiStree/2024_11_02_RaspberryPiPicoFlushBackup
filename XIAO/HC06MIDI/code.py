# Test your controller: https://hardwaretester.com/gamepad
import board  # type: ignore (this is a CircuitPython built-in)
from joystick_xl.inputs import Axis, Button, Hat
from joystick_xl.joystick import Joystick
import time
import usb_midi
import adafruit_midi
import digitalio
import busio
import analogio

from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], in_channel=0,midi_out=usb_midi.ports[1], out_channel=0)
joystick = Joystick()

#RASPBERRY PI PICO rx=1 tx=0
#SEEED XIAO RP2040 rx=6 tx=7
hc05 = busio.UART(board.TX, board.RX, baudrate=9600, timeout=0)

maxAnalogValue=65535
#maxAnalogValue=1023
#maxAnalogValue=255

use_print_log=False
use_hardware_joystick=True
c5=""
c4=""
c3=""
c2=""
c1=""
c0=""
string_msg=""
string_val=""
#i =0
joystick.add_input()
joystick.update(False)
if use_print_log:
    print("JS "+str(joystick.num_axes)+" "+ str(joystick.num_buttons)+" "+ str(joystick.num_hats))
    print("JS "+str(len(joystick.axis))+" "+ str(len(joystick.button))+" "+ str(len(joystick.hat)))
readTime1=None
readTime2=None

#Test all axis : M3 Z3 m3 z3 M4 Z4 m4 z4 H2 M2 Z2 c2
        
isInFloatMode=False
isInIndexMode=True
value=0.999



############### SEEED XIAO RP2040  START
# Create analog input objects for GPIO 0, 1, 2, and 3
analog_pins = [board.A0, board.A1, board.A2, board.A3]
analog_pins_axis_index=[0,1,2,3]
analog_pins_axis_use=[True, False, False, False]
analog_inputs = [analogio.AnalogIn(pin) for pin in analog_pins]

# Create digital input objects for GPIO 4, 5, 8, 9, and 10
digital_pins = [board.D4, board.D5, board.D8, board.D9, board.D10]
digital_index=[0,1,2,3,4]
digital_use=[True, False, True, False, False]
digital_inputs = [digitalio.DigitalInOut(pin) for pin in digital_pins]

# Set the direction of digital pins as input
for pin in digital_inputs:
    pin.direction = digitalio.Direction.INPUT

############### SEEED XIAO RP2040  END


def isDoubleCharCMD(charValue):
    return charValue=='0' or charValue=='1' or charValue=='2' or charValue=='3' or charValue=='4' or charValue=='5' or charValue=='6' or charValue=='7' or charValue=='8' or charValue=='9' or charValue=='%'or charValue=='='or charValue=='~' 

def setButtonTo(intIndexButton,boolState):
    
    if use_print_log:
        print("BUT"+str(intIndexButton)+" "+str(boolState))
    if boolState:
        joystick.update_button((intIndexButton, True))
        midi.send(NoteOn(intIndexButton, 120))
    else:
        joystick.update_button((intIndexButton, False))
        midi.send(NoteOff(intIndexButton, 0))
      
valuej=0
valuem=0

    
def setJoystickFloatPercentTo(intIndexButton,flaotN1ToP1):
    valuej =int((flaotN1ToP1 + 1.0)/2.0 * 255.0)
    if valuej>=255:
        valuej=255
    if valuej<=0:
        valuej=0
    valuem =int((flaotN1ToP1 + 1.0)/2.0 * 127.0)
    if valuem>=127:
        valuem=127
    if valuem<=0:
        valuem=0
    if use_print_log:
        print(valuej)
        print(valuem)
    if flaotN1ToP1==0:
        setJoystickInt255127To(intIndexButton,128,62) 
    else:
        setJoystickInt255127To(intIndexButton,valuej,valuem)
    
    
def setJoystickFloatPercent01To(intIndexButton,flaotN0ToP1):
    setJoystickFloatPercentTo(intIndexButton, (flaotN0ToP1*2.0)-1)
    
def setJoystickInt255127To(intIndexButton,intAxis0To255, intMidi0To127):
    if use_print_log:
        print("JOY255 "+str(intIndexButton)+ " "+str(intAxis0To255))
    joystick.update_axis((intIndexButton, intAxis0To255))
    midi.send(ControlChange(intIndexButton, intMidi0To127))
    
valuem=0
def setAxis08To(intIndexButton,intAxis0To8):
    valuem=round( 127.0*(intAxis0To8 / 8.0))
    if use_print_log:
        print("PAD"+str(intIndexButton))
    joystick.update_hat((intIndexButton, intAxis0To8))
    midi.send(ControlChange(8+intIndexButton,valuem ))

    
                
def pushChar(charValue):
    global c5
    global c4
    global c3
    global c2
    global c1
    global c0
    c5=c4
    c4=c3
    c3=c2
    c2=c1
    c1=c0
    c0=charValue
    #print("C1:"+str(c1)+" "+str(c2))
    if isDoubleCharCMD(c0) or isInFloatMode:
        executeDoubleCharCMD()
        #print("CC1:"+str(c1)+" "+str(c2))


def executeDoubleCharCMD():
    #  . < ( + | & ! $ * ) ; ¬ - / , % _ > ?: # @ ' = " ~ {}
    #ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz
        global isInFloatMode
        global isInIndexMode
        global use_hardware_joystick

        #if use_print_log:
        print("Char CMD:"+ str(c5) +" "+ str(c4) +" "+ str(c3)+" "+str(c2)+" "+str(c1)+" "+str(c0))
            
        if c1== '0' and c0=='=' :
            joystick.reset_all()
            print("Reset all joystick")
        elif c1=='J' and c0=='=':
            use_hardware_joystick=True
            print("Start listening to Joystick")
        elif c1=='j' and c0=='=':
            use_hardware_joystick=False
            print("Stop listening to Joystick")
        
        elif( c0=='%'):
            isInFloatMode=True
            isInIndexMode=False
            print("Float Mode")
        elif(c0=='~'):
            isInFloatMode=False
            isInIndexMode=True
            print("Index Table Mode")
            # Most of the time it is ok to use Axis with 1 0.7 0.1 but some time you need precise value. 
            # That means that is slower to received too as there are more byte to received.
            # #-29998 +29999 Put Axis 2 to -0.9998 1.0 

        # % 000 A  A is the index and the sign % Means that a float value is to read and the 000 is the value.
        elif isInFloatMode:
            if( c4=='%'):
                try:
                    value= int(c3)*0.1
                    value+= int(c2)*0.01
                    value+= int(c1)*0.001
                except Exception as e:
                    value = 0
                    
                print("="+c0+" "+str(value))
                if c0=="A": 
                    setJoystickFloatPercentTo(0,value)
                elif c0=="a": 
                    setJoystickFloatPercentTo(0,-value)
                elif c0=="B": 
                    setJoystickFloatPercentTo(1,value)
                elif c0=="b": 
                    setJoystickFloatPercentTo(1,-value)
                elif c0=="C": 
                    setJoystickFloatPercentTo(2,value)
                elif c0=="c": 
                    setJoystickFloatPercentTo(2,-value)
                elif c0=="D": 
                    setJoystickFloatPercentTo(3,value)
                elif c0=="d": 
                    setJoystickFloatPercentTo(3,-value)
                elif c0=="E": 
                    setJoystickFloatPercentTo(4,value)
                elif c0=="e": 
                    setJoystickFloatPercentTo(4,-value)
                elif c0=="F": 
                    setJoystickFloatPercentTo(5,value)
                elif c0=="f": 
                    setJoystickFloatPercentTo(5,-value)
                elif c0=="G": 
                    setJoystickFloatPercentTo(6,value)
                elif c0=="g": 
                    setJoystickFloatPercentTo(6,-value)
                elif c0=="H": 
                    setJoystickFloatPercentTo(7,value)
                elif c0=="h": 
                    setJoystickFloatPercentTo(7,-value)
                    


        elif isInIndexMode:
            if c0== '1' :
                if c1=='A':
                    setButtonTo( 0,True)
                elif c1=='B': 
                    setButtonTo( 1,True)
                elif c1=='C': 
                    setButtonTo( 2,True)
                elif c1=='D': 
                    setButtonTo( 3,True)
                elif c1=='E': 
                    setButtonTo( 4,True)
                elif c1=='F': 
                    setButtonTo( 5,True)
                elif c1=='G': 
                    setButtonTo( 6,True)
                elif c1=='H': 
                    setButtonTo( 7,True)
                elif c1=='I': 
                    setButtonTo( 8,True)
                elif c1=='J': 
                    setButtonTo( 9,True)
                elif c1=='K':
                    setButtonTo(10,True)
                elif c1=='L':
                    setButtonTo(11,True)
                elif c1=='M':
                    setButtonTo(12,True)
                elif c1=='N':
                    setButtonTo(13,True)
                elif c1=='O':
                    setButtonTo(14,True)
                elif c1=='P':
                    setButtonTo(15,True)
                elif c1=='Q':
                    setButtonTo(16,True)
                elif c1=='R':
                    setButtonTo(17,True)
                elif c1=='S':
                    setButtonTo(18,True)
                elif c1=='T':
                    setButtonTo(19,True)
                elif c1=='U':
                    setButtonTo(20,True)
                elif c1=='V':
                    setButtonTo(21,True)
                elif c1=='W':
                    setButtonTo(22,True)
                elif c1=='X':
                    setButtonTo(23,True)
                elif c1=='Y':
                    setButtonTo(24,True)
                elif c1=='Z':
                    setButtonTo(25,True)
                elif c1=='a':
                    setButtonTo(26,True)
                elif c1=='b':
                    setButtonTo(27,True)
                elif c1=='c':
                    setButtonTo(28,True)
                elif c1=='d':
                    setButtonTo(29,True)
                elif c1=='e':
                    setButtonTo(30,True)
                elif c1=='f':
                    setButtonTo(31,True)
                elif c1=='g':
                    setButtonTo(32,True)
                elif c1=='h':
                    setButtonTo(33,True)
                elif c1=='i':
                    setButtonTo(34,True)
                elif c1=='j':
                    setButtonTo(35,True)
                elif c1=='k':
                    setButtonTo(36,True)
                elif c1=='l':
                    setButtonTo(37,True)
                elif c1=='m':
                    setButtonTo(38,True)
                elif c1=='n':
                    setButtonTo(39,True)
                elif c1=='o':
                    setButtonTo(40,True)
                elif c1=='p':
                    setButtonTo(41,True)
                elif c1=='q':
                    setButtonTo(42,True)
                elif c1=='r':
                    setButtonTo(43,True)
                elif c1=='s':
                    setButtonTo(44,True)
                elif c1=='t':
                    setButtonTo(45,True)
                elif c1=='u':
                    setButtonTo(46,True)
                elif c1=='v':
                    setButtonTo(47,True)
                elif c1=='w':
                    setButtonTo(48,True)
                elif c1=='x':
                    setButtonTo(49,True)
                elif c1=='y':
                    setButtonTo(50,True)
                elif c1=='z':
                    setButtonTo(51,True)

            if c0== '0' :
                if c1=='A':
                    setButtonTo(0,False)
                elif c1=='B':
                    setButtonTo(1,False)
                elif c1=='C':
                    setButtonTo(2,False)
                elif c1=='D':
                    setButtonTo(3,False)
                elif c1=='E':
                    setButtonTo(4,False)
                elif c1=='F':
                    setButtonTo(5,False)
                elif c1=='G':
                    setButtonTo(6,False)
                elif c1=='H':
                    setButtonTo(7,False)
                elif c1=='I':
                    setButtonTo(8,False)
                elif c1=='J':
                    setButtonTo(9,False)
                elif c1=='K':
                    setButtonTo(10,False)
                elif c1=='L':
                    setButtonTo(11,False)
                elif c1=='M':
                    setButtonTo(12,False)
                elif c1=='N':
                    setButtonTo(13,False)
                elif c1=='O':
                    setButtonTo(14,False)
                elif c1=='P':
                    setButtonTo(15,False)
                elif c1=='Q':
                    setButtonTo(16,False)
                elif c1=='R':
                    setButtonTo(17,False)
                elif c1=='S':
                    setButtonTo(18,False)
                elif c1=='T':
                    setButtonTo(19,False)
                elif c1=='U':
                    setButtonTo(20,False)
                elif c1=='V':
                    setButtonTo(21,False)
                elif c1=='W':
                    setButtonTo(22,False)
                elif c1=='X':
                    setButtonTo(23,False)
                elif c1=='Y':
                    setButtonTo(24,False)
                elif c1=='Z':
                    setButtonTo(25,False)
                elif c1=='a':
                    setButtonTo(26,False)
                elif c1=='b':
                    setButtonTo(27,False)
                elif c1=='c':
                    setButtonTo(28,False)
                elif c1=='d':
                    setButtonTo(29,False)
                elif c1=='e':
                    setButtonTo(30,False)
                elif c1=='f':
                    setButtonTo(31,False)
                elif c1=='g':
                    setButtonTo(32,False)
                elif c1=='h':
                    setButtonTo(33,False)
                elif c1=='i':
                    setButtonTo(34,False)
                elif c1=='j':
                    setButtonTo(35,False)
                elif c1=='k':
                    setButtonTo(36,False)
                elif c1=='l':
                    setButtonTo(37,False)
                elif c1=='m':
                    setButtonTo(38,False)
                elif c1=='n':
                    setButtonTo(39,False)
                elif c1=='o':
                    setButtonTo(40,False)
                elif c1=='p':
                    setButtonTo(41,False)
                elif c1=='q':
                    setButtonTo(42,False)
                elif c1=='r':
                    setButtonTo(43,False)
                elif c1=='s':
                    setButtonTo(44,False)
                elif c1=='t':
                    setButtonTo(45,False)
                elif c1=='u':
                    setButtonTo(46,False)
                elif c1=='v':
                    setButtonTo(47,False)
                elif c1=='w':
                    setButtonTo(48,False)
                elif c1=='x':
                    setButtonTo(49,False)
                elif c1=='y':
                    setButtonTo(50,False)
                elif c1=='z':
                    setButtonTo(51,False)
      
                    
            if c0== '3' :
                if c1=='A':
                    setButtonTo(52, True)
                elif c1=='B': 
                    setButtonTo(53, True)
                elif c1=='C': 
                    setButtonTo(54, True)
                elif c1=='D': 
                    setButtonTo(55, True)
                elif c1=='E': 
                    setButtonTo(56, True)
                elif c1=='F': 
                    setButtonTo(57, True)
                elif c1=='G': 
                    setButtonTo(58, True)
                elif c1=='H': 
                    setButtonTo(59, True)
                elif c1=='I': 
                    setButtonTo(60, True)
                elif c1=='J': 
                    setButtonTo(61, True)
                elif c1=='K': 
                    setButtonTo(62, True)
                elif c1=='L': 
                    setButtonTo(63, True)
                elif c1=='M': 
                    setButtonTo(64, True)
                elif c1=='N': 
                    setButtonTo(65, True)
                elif c1=='O': 
                    setButtonTo(66, True)
                elif c1=='P': 
                    setButtonTo(67, True)
                elif c1=='Q': 
                    setButtonTo(68, True)
                elif c1=='R': 
                    setButtonTo(69, True)
                elif c1=='S': 
                    setButtonTo(70, True)
                elif c1=='T': 
                    setButtonTo(71, True)
                elif c1=='U': 
                    setButtonTo(72, True)
                elif c1=='V': 
                    setButtonTo(73, True)
                elif c1=='W': 
                    setButtonTo(74, True)
                elif c1=='X': 
                    setButtonTo(75, True)
                elif c1=='Y': 
                    setButtonTo(76, True)
                elif c1=='Z': 
                    setButtonTo(77, True)
                elif c1=='a': 
                    setButtonTo(78, True)
                elif c1=='b': 
                    setButtonTo(79, True)
                elif c1=='c': 
                    setButtonTo(80, True)
                elif c1=='d': 
                    setButtonTo(81, True)
                elif c1=='e': 
                    setButtonTo(82, True)
                elif c1=='f': 
                    setButtonTo(83, True)
                elif c1=='g': 
                    setButtonTo(84, True)
                elif c1=='h': 
                    setButtonTo(85, True)
                elif c1=='i': 
                    setButtonTo(86, True)
                elif c1=='j': 
                    setButtonTo(87, True)
                elif c1=='k': 
                    setButtonTo(88, True)
                elif c1=='l': 
                    setButtonTo(89, True)
                elif c1=='m': 
                    setButtonTo(90, True)
                elif c1=='n': 
                    setButtonTo(91, True)
                elif c1=='o': 
                    setButtonTo(92, True)
                elif c1=='p': 
                    setButtonTo(93, True)
                elif c1=='q': 
                    setButtonTo(94, True)
                elif c1=='r': 
                    setButtonTo(95, True)
                elif c1=='s': 
                    setButtonTo(96, True)
                elif c1=='t': 
                    setButtonTo(97, True)
                elif c1=='u': 
                    setButtonTo(98, True)
                elif c1=='v': 
                    setButtonTo(99, True)
                elif c1=='w':
                    setButtonTo(100,True)
                elif c1=='x':
                    setButtonTo(101,True)
                elif c1=='y':
                    setButtonTo(102,True)
                elif c1=='z':
                    setButtonTo(103,True)

            if c0== '2' :
                if c1=='A':
                    setButtonTo(52, False)
                elif c1=='B': 
                    setButtonTo(53, False)
                elif c1=='C': 
                    setButtonTo(54, False)
                elif c1=='D': 
                    setButtonTo(55, False)
                elif c1=='E': 
                    setButtonTo(56, False)
                elif c1=='F': 
                    setButtonTo(57, False)
                elif c1=='G': 
                    setButtonTo(58, False)
                elif c1=='H': 
                    setButtonTo(59, False)
                elif c1=='I': 
                    setButtonTo(60, False)
                elif c1=='J': 
                    setButtonTo(61, False)
                elif c1=='K':
                    setButtonTo(62, False)
                elif c1=='L':
                    setButtonTo(63, False)
                elif c1=='M':
                    setButtonTo(64, False)
                elif c1=='N':
                    setButtonTo(65, False)
                elif c1=='O':
                    setButtonTo(66, False)
                elif c1=='P':
                    setButtonTo(67, False)
                elif c1=='Q':
                    setButtonTo(68, False)
                elif c1=='R':
                    setButtonTo(69, False)
                elif c1=='S':
                    setButtonTo(70, False)
                elif c1=='T':
                    setButtonTo(71, False)
                elif c1=='U':
                    setButtonTo(72, False)
                elif c1=='V':
                    setButtonTo(73, False)
                elif c1=='W':
                    setButtonTo(74, False)
                elif c1=='X':
                    setButtonTo(75, False)
                elif c1=='Y':
                    setButtonTo(76, False)
                elif c1=='Z':
                    setButtonTo(77, False)
                elif c1=='a':
                    setButtonTo(78, False)
                elif c1=='b':
                    setButtonTo(79, False)
                elif c1=='c':
                    setButtonTo(80, False)
                elif c1=='d':
                    setButtonTo(81, False)
                elif c1=='e':
                    setButtonTo(82, False)
                elif c1=='f':
                    setButtonTo(83, False)
                elif c1=='g':
                    setButtonTo(84, False)
                elif c1=='h':
                    setButtonTo(85, False)
                elif c1=='i':
                    setButtonTo(86, False)
                elif c1=='j':
                    setButtonTo(87, False)
                elif c1=='k':
                    setButtonTo(88, False)
                elif c1=='l':
                    setButtonTo(89, False)
                elif c1=='m':
                    setButtonTo(90, False)
                elif c1=='n':
                    setButtonTo(91, False)
                elif c1=='o':
                    setButtonTo(92, False)
                elif c1=='p':
                    setButtonTo(93, False)
                elif c1=='q':
                    setButtonTo(94, False)
                elif c1=='r':
                    setButtonTo(95, False)
                elif c1=='s':
                    setButtonTo(96, False)
                elif c1=='t':
                    setButtonTo(97, False)
                elif c1=='u':
                    setButtonTo(98, False)
                elif c1=='v':
                    setButtonTo(99, False)
                elif c1=='w':
                    setButtonTo(100,False)
                elif c1=='x':
                    setButtonTo(101,False)
                elif c1=='y':
                    setButtonTo(102,False)
                elif c1=='z':
                    setButtonTo(103,False)

            if c0== '5' :
                if c1=='A':
                    setButtonTo(104, True)
                elif c1=='B': 
                    setButtonTo(105, True)
                elif c1=='C': 
                    setButtonTo(106, True)
                elif c1=='D': 
                    setButtonTo(107, True)
                elif c1=='E': 
                    setButtonTo(108, True)
                elif c1=='F': 
                    setButtonTo(109, True)
                elif c1=='G': 
                    setButtonTo(110, True)
                elif c1=='H': 
                    setButtonTo(111, True)
                elif c1=='I': 
                    setButtonTo(112, True)
                elif c1=='J': 
                    setButtonTo(113, True)
                elif c1=='K': 
                    setButtonTo(114, True)
                elif c1=='L': 
                    setButtonTo(115, True)
                elif c1=='M': 
                    setButtonTo(116, True)
                elif c1=='N': 
                    setButtonTo(117, True)
                elif c1=='O': 
                    setButtonTo(118, True)
                elif c1=='P': 
                    setButtonTo(119, True)
                elif c1=='Q': 
                    setButtonTo(120, True)
                elif c1=='R': 
                    setButtonTo(121, True)
                elif c1=='S': 
                    setButtonTo(122, True)
                elif c1=='T': 
                    setButtonTo(123, True)
                elif c1=='U': 
                    setButtonTo(124, True)
                elif c1=='V': 
                    setButtonTo(125, True)
                elif c1=='W': 
                    setButtonTo(126, True)
                elif c1=='X': 
                    setButtonTo(127, True)
                

            if c0== '4' :
                if c1=='A':
                    setButtonTo(104, False)
                elif c1=='B': 
                    setButtonTo(105, False)
                elif c1=='C': 
                    setButtonTo(106, False)
                elif c1=='D': 
                    setButtonTo(107, False)
                elif c1=='E': 
                    setButtonTo(108, False)
                elif c1=='F': 
                    setButtonTo(109, False)
                elif c1=='G': 
                    setButtonTo(110, False)
                elif c1=='H': 
                    setButtonTo(111, False)
                elif c1=='I': 
                    setButtonTo(112, False)
                elif c1=='J': 
                    setButtonTo(113, False)
                elif c1=='K':
                    setButtonTo(114, False)
                elif c1=='L':
                    setButtonTo(115, False)
                elif c1=='M':
                    setButtonTo(116, False)
                elif c1=='N':
                    setButtonTo(117, False)
                elif c1=='O':
                    setButtonTo(118, False)
                elif c1=='P':
                    setButtonTo(119, False)
                elif c1=='Q':
                    setButtonTo(120, False)
                elif c1=='R':
                    setButtonTo(121, False)
                elif c1=='S':
                    setButtonTo(122, False)
                elif c1=='T':
                    setButtonTo(123, False)
                elif c1=='U':
                    setButtonTo(124, False)
                elif c1=='V':
                    setButtonTo(125, False)
                elif c1=='W':
                    setButtonTo(126, False)
                elif c1=='X':
                    setButtonTo(127, False)
              




            if c0== '6' :
                if c1=='A':
                    setAxis08To(0,0)
                elif c1=='B':
                    setAxis08To(0,1)
                elif c1=='C':
                    setAxis08To(0,2)
                elif c1=='D':
                    setAxis08To(0,3)
                elif c1=='E':
                    setAxis08To(0,4)
                elif c1=='F':
                    setAxis08To(0,5)
                elif c1=='G':
                    setAxis08To(0,6)
                elif c1=='H':
                    setAxis08To(0,7)
                elif c1=='I':
                    setAxis08To(0,8)
                elif c1=='J':
                    setAxis08To(1,0)
                elif c1=='K':
                    setAxis08To(1,1)
                elif c1=='L':
                    setAxis08To(1,2)
                elif c1=='M':
                    setAxis08To(1,3)
                elif c1=='N':
                    setAxis08To(1,4)
                elif c1=='O':
                    setAxis08To(1,5)
                elif c1=='P':
                    setAxis08To(1,6)
                elif c1=='Q':
                    setAxis08To(1,7)
                elif c1=='R':
                    setAxis08To(1,8)
                elif c1=='S':
                    setAxis08To(2,0)
                elif c1=='T':
                    setAxis08To(2,1)
                elif c1=='U':
                    setAxis08To(2,2)
                elif c1=='V':
                    setAxis08To(2,3)
                elif c1=='W':
                    setAxis08To(2,4)
                elif c1=='X':
                    setAxis08To(2,5)
                elif c1=='Y':
                    setAxis08To(2,6)
                elif c1=='Z':
                    setAxis08To(2,7)
                elif c1=='a':
                    setAxis08To(2,8)
                elif c1=='a':
                    setAxis08To(3,0)
                elif c1=='b':
                    setAxis08To(3,1)
                elif c1=='c':
                    setAxis08To(3,2)
                elif c1=='d':
                    setAxis08To(3,3)
                elif c1=='e':
                    setAxis08To(3,4)
                elif c1=='f':
                    setAxis08To(3,5)
                elif c1=='g':
                    setAxis08To(3,6)
                elif c1=='h':
                    setAxis08To(3,7)
                elif c1=='i':
                    setAxis08To(3,8)
 
            if c0== '8' :
                if c1=='A':
                    setJoystickFloatPercentTo(0,-1.0)
                elif c1=='B':
                    setJoystickFloatPercentTo(0,-0.9)
                elif c1=='C':
                    setJoystickFloatPercentTo(0,-0.8)
                elif c1=='D':
                    setJoystickFloatPercentTo(0,-0.5)
                elif c1=='E':
                    setJoystickFloatPercentTo(0,-0.25)
                elif c1=='F':
                    setJoystickFloatPercentTo(0,0.1)
                elif c1=='G':
                    setJoystickFloatPercentTo(0,0)
                elif c1=='H':
                    setJoystickFloatPercentTo(0,0.1)
                elif c1=='I':
                    setJoystickFloatPercentTo(0,0.25)
                elif c1=='J':
                    setJoystickFloatPercentTo(0,0.50)
                elif c1=='K':
                    setJoystickFloatPercentTo(0,0.8)
                elif c1=='L':
                    setJoystickFloatPercentTo(0,0.9)
                elif c1=='M':
                    setJoystickFloatPercentTo(0,1.0)

                elif c1=='N':
                    setJoystickFloatPercentTo(1,-1.0)
                elif c1=='O':
                    setJoystickFloatPercentTo(1,-0.9)
                elif c1=='P':
                    setJoystickFloatPercentTo(1,-0.8)
                elif c1=='Q':
                    setJoystickFloatPercentTo(1,-0.5)
                elif c1=='R':
                    setJoystickFloatPercentTo(1,-0.25)
                elif c1=='S':
                    setJoystickFloatPercentTo(1,0.1)
                elif c1=='T':
                    setJoystickFloatPercentTo(1,0)
                elif c1=='U':
                    setJoystickFloatPercentTo(1,0.1)
                elif c1=='V':
                    setJoystickFloatPercentTo(1,0.25)
                elif c1=='W':
                    setJoystickFloatPercentTo(1,0.50)
                elif c1=='X':
                    setJoystickFloatPercentTo(1,0.8)
                elif c1=='Y':
                    setJoystickFloatPercentTo(1,0.9)
                elif c1=='Z':
                    setJoystickFloatPercentTo(1,1.0)

                elif c1=='a':
                    setJoystickFloatPercentTo(2,-1.0)
                elif c1=='b':
                    setJoystickFloatPercentTo(2,-0.9)
                elif c1=='c':
                    setJoystickFloatPercentTo(2,-0.8)
                elif c1=='d':
                    setJoystickFloatPercentTo(2,-0.5)
                elif c1=='e':
                    setJoystickFloatPercentTo(2,-0.25)
                elif c1=='f':
                    setJoystickFloatPercentTo(2,0.1)
                elif c1=='g':
                    setJoystickFloatPercentTo(2,0)
                elif c1=='h':
                    setJoystickFloatPercentTo(2,0.1)
                elif c1=='i':
                    setJoystickFloatPercentTo(2,0.25)
                elif c1=='j':
                    setJoystickFloatPercentTo(2,0.50)
                elif c1=='k':
                    setJoystickFloatPercentTo(2,0.8)
                elif c1=='l':
                    setJoystickFloatPercentTo(2,0.9)
                elif c1=='m':
                    setJoystickFloatPercentTo(2,1.0)

                elif c1=='n':
                    setJoystickFloatPercentTo(3,-1.0)
                elif c1=='o':
                    setJoystickFloatPercentTo(3,-0.9)
                elif c1=='p':
                    setJoystickFloatPercentTo(3,-0.8)
                elif c1=='q':
                    setJoystickFloatPercentTo(3,-0.5)
                elif c1=='r':
                    setJoystickFloatPercentTo(3,-0.25)
                elif c1=='s':
                    setJoystickFloatPercentTo(3,0.1)
                elif c1=='t':
                    setJoystickFloatPercentTo(3,0)
                elif c1=='u':
                    setJoystickFloatPercentTo(3,0.1)
                elif c1=='v':
                    setJoystickFloatPercentTo(3,0.25)
                elif c1=='w':
                    setJoystickFloatPercentTo(3,0.50)
                elif c1=='x':
                    setJoystickFloatPercentTo(3,0.8)
                elif c1=='y':
                    setJoystickFloatPercentTo(3,0.9)
                elif c1=='z':
                    setJoystickFloatPercentTo(3,1.0)

            if c0== '9' :
                if c1=='A':
                    setJoystickFloatPercentTo(4,-1.0)
                elif c1=='B':
                    setJoystickFloatPercentTo(4,-0.9)
                elif c1=='C':
                    setJoystickFloatPercentTo(4,-0.8)
                elif c1=='D':
                    setJoystickFloatPercentTo(4,-0.5)
                elif c1=='E':
                    setJoystickFloatPercentTo(4,-0.25)
                elif c1=='F':
                    setJoystickFloatPercentTo(4,0.1)
                elif c1=='G':
                    setJoystickFloatPercentTo(4,0)
                elif c1=='H':
                    setJoystickFloatPercentTo(4,0.1)
                elif c1=='I':
                    setJoystickFloatPercentTo(4,0.25)
                elif c1=='J':
                    setJoystickFloatPercentTo(4,0.50)
                elif c1=='K':
                    setJoystickFloatPercentTo(4,0.8)
                elif c1=='L':
                    setJoystickFloatPercentTo(4,0.9)
                elif c1=='M':
                    setJoystickFloatPercentTo(4,1.0)

                elif c1=='N':
                    setJoystickFloatPercentTo(5,-1.0)
                elif c1=='O':
                    setJoystickFloatPercentTo(5,-0.9)
                elif c1=='P':
                    setJoystickFloatPercentTo(5,-0.8)
                elif c1=='Q':
                    setJoystickFloatPercentTo(5,-0.5)
                elif c1=='R':
                    setJoystickFloatPercentTo(5,-0.25)
                elif c1=='S':
                    setJoystickFloatPercentTo(5,0.1)
                elif c1=='T':
                    setJoystickFloatPercentTo(5,0)
                elif c1=='U':
                    setJoystickFloatPercentTo(5,0.1)
                elif c1=='V':
                    setJoystickFloatPercentTo(5,0.25)
                elif c1=='W':
                    setJoystickFloatPercentTo(5,0.50)
                elif c1=='X':
                    setJoystickFloatPercentTo(5,0.8)
                elif c1=='Y':
                    setJoystickFloatPercentTo(5,0.9)
                elif c1=='Z':
                    setJoystickFloatPercentTo(5,1.0)

                elif c1=='a':
                    setJoystickFloatPercentTo(6,-1.0)
                elif c1=='b':
                    setJoystickFloatPercentTo(6,-0.9)
                elif c1=='c':
                    setJoystickFloatPercentTo(6,-0.8)
                elif c1=='d':
                    setJoystickFloatPercentTo(6,-0.5)
                elif c1=='e':
                    setJoystickFloatPercentTo(6,-0.25)
                elif c1=='f':
                    setJoystickFloatPercentTo(6,0.1)
                elif c1=='g':
                    setJoystickFloatPercentTo(6,0)
                elif c1=='h':
                    setJoystickFloatPercentTo(6,0.1)
                elif c1=='i':
                    setJoystickFloatPercentTo(6,0.25)
                elif c1=='j':
                    setJoystickFloatPercentTo(6,0.50)
                elif c1=='k':
                    setJoystickFloatPercentTo(6,0.8)
                elif c1=='l':
                    setJoystickFloatPercentTo(6,0.9)
                elif c1=='m':
                    setJoystickFloatPercentTo(6,1.0)

                elif c1=='n':
                    setJoystickFloatPercentTo(7,-1.0)
                elif c1=='o':
                    setJoystickFloatPercentTo(7,-0.9)
                elif c1=='p':
                    setJoystickFloatPercentTo(7,-0.8)
                elif c1=='q':
                    setJoystickFloatPercentTo(7,-0.5)
                elif c1=='r':
                    setJoystickFloatPercentTo(7,-0.25)
                elif c1=='s':
                    setJoystickFloatPercentTo(7,0.1)
                elif c1=='t':
                    setJoystickFloatPercentTo(7,0)
                elif c1=='u':
                    setJoystickFloatPercentTo(7,0.1)
                elif c1=='v':
                    setJoystickFloatPercentTo(7,0.25)
                elif c1=='w':
                    setJoystickFloatPercentTo(7,0.50)
                elif c1=='x':
                    setJoystickFloatPercentTo(7,0.8)
                elif c1=='y':
                    setJoystickFloatPercentTo(7,0.9)
                elif c1=='z':
                    setJoystickFloatPercentTo(7,1.0)

      


while True:
    
    if use_hardware_joystick:
        # Read analog values
        for i, analog_input in enumerate(analog_inputs):
            if i==0:
                print(f"Analog {i}: {analog_input.value}")
            if analog_pins_axis_use[i]:
                setJoystickFloatPercent01To(analog_pins_axis_index[i],analog_input.value/maxAnalogValue)

        # Read digital states
        for i, digital_input in enumerate(digital_inputs):
            if digital_use[i]:
                setButtonTo(digital_index[i], digital_input.value)
    
    msg = midi.receive()
    if msg is not None:
        if use_print_log:
            print("Received MIDI:", msg, "at", time.monotonic())
    if msg is not None:
        #  if a NoteOn message...
        if isinstance(msg, NoteOn):
            if msg.note>=0 and msg.note <= 128:
                joystick.update_button((msg.note, True))
            string_msg = 'NoteOn'
            #  get note number
            string_val = str(msg.note)
            midi.send(NoteOn(msg.note, 120))
            
        #  if a NoteOff message...
        if isinstance(msg, NoteOff):
            if msg.note>=0 and msg.note <= 128:
                joystick.update_button((msg.note, False))
            string_msg = 'NoteOff'
            #  get note number
            string_val = str(msg.note)
            midi.send(NoteOff(msg.note, 0))
        #  if a PitchBend message...
        if isinstance(msg, PitchBend):
            string_msg = 'PitchBend'
            #  get value of pitchbend
            string_val = str(msg.pitch_bend)
        #  if a CC message...
        if isinstance(msg, ControlChange):
            string_msg = 'ControlChange'
            if msg.control>=0 and msg.control <= 7:
                joystick.update_axis((msg.control, msg.value*2))
            #  get CC message number
            string_val = str(msg.control) +" "+str(msg.value)
        #  update text area with message type and value of message as strings
        if use_print_log:
            print(string_msg+"->"+string_val)
        
    readTime1= time.monotonic_ns()/ 1_000_000.0
    blemsgbytes=hc05.read(1)
    readTime2= time.monotonic_ns()/ 1_000_000.0


    if blemsgbytes != None:
        T1 = "{:.6f}".format(readTime1)
        T2 = "{:.6f}".format(readTime2)
        if use_print_log:
            print("Time MS: " (T1)+ " "+ (T2))
        #15036365234375 #15037031250000
        #B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5B1C3D5
        blemsg=blemsgbytes.decode()
        
        if len(blemsg)==1:
            pushChar(blemsg[0])
            
            

        