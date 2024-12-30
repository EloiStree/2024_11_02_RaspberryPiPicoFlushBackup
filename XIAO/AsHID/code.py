#import board support libraries, including HID.
import board
import digitalio
import analogio
import usb_hid
import random

from time import sleep

#Libraries for communicating as a Keyboard device
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

#library for communicating as a gamepad
from hid_gamepad import Gamepad

from adafruit_hid.mouse import Mouse
mouse = Mouse(usb_hid.devices)

from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl

mediacontrol = ConsumerControl(usb_hid.devices)

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
gp = Gamepad(usb_hid.devices)

#Create a collection of GPIO pins that represent the buttons
#This includes the digital pins for the Directional Pad.
#They can be used as regular buttons if using the analog inputs instead
button_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7,board.GP10, board.GP11)



# Map the buttons to button numbers on the Gamepad.
# gamepad_buttons[i] will send that button number when buttons[i]
# is pushed.
gamepad_buttons = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

#Keyboard Mode Button Definitions
keyboard_buttons = {0 : Keycode.UP_ARROW, 1 : Keycode.LEFT_ARROW, 2 : Keycode.DOWN_ARROW, 3 : Keycode.RIGHT_ARROW,
                  4 : Keycode.LEFT_CONTROL, 5 : Keycode.SPACE, 6 : Keycode.W, 7 : Keycode.ENTER, 8 : Keycode.LEFT_ALT
                    , 9 : Keycode.ENTER}

#FPS Mode Button Definitions
fps_buttons = {0 : Keycode.W, 1 : Keycode.A, 2 : Keycode.S, 3 : Keycode.D,
                  4 : Keycode.LEFT_CONTROL, 5 : Keycode.SPACE, 6 : Keycode.LEFT_ALT, 7 : Keycode.ENTER,
               8 : Keycode.ENTER, 9: Keycode.ENTER }

#List of defind mode names
mode_names = {1 : 'Gamepad', 2 : 'Keyboard', 3 : 'FPS', 4 : "Mouse", 5 : "Multimedia"}

#Set Default Mode To 1
mode = 1



# Setup for Analog Joystick as X and Y
#ax = analogio.AnalogIn(board.GP26)
#ay = analogio.AnalogIn(board.GP27)



# Equivalent of Arduino's map() function.
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
  


text = "Mode : " + str(mode)

def debounce():
    sleep(0.2)


#print("Hello")

index = 1
setx = 0
sety = 0


while True:
    
    index = index + 1
    
    #Check to see if the mode change button is pressed
    if mode == 1:
        gp.move_joysticks(
            x=(int)( random.uniform(-1.0, 1.0) * 127 ),
            y=(int)( random.uniform(-0.7, 0.7) * 127 ),
            z=(int)( random.uniform(-0.5, 0.5) * 127 ),
            r_z=(int)( random.uniform(-0.1, 0.1) * 127 )
        )
        if index > 16:
            index = 1
            
        gp.press_buttons(index)
        sleep(0.3)
        gp.release_buttons(index)
            
                #print(gamepad_button_num)
        
#    if mode == 2: # Keyboard Mode
 #           
  #      for i, button in enumerate(buttons):
   #         if button.value:
    #            keyboard.release(keyboard_buttons[i])
     #       else:
      #          keyboard.press(keyboard_buttons[i]) 
    
    #FPS Mode
#    if mode == 3:
  #      for i, button in enumerate(buttons):
   #         gamepad_button_num = gamepad_buttons[i]
    #        if button.value:
     #           keyboard.release(fps_buttons[i])
     #       else:
      #          keyboard.press(fps_buttons[i])
                
#    if mode == 4:
 #       if not buttons[0].value:
 #           mouse.move(y=-4)
  #      if not buttons[2].value:
  #          mouse.move(y=4)
  #      if not buttons[1].value:
  #          mouse.move(x=-4)
  #      if not buttons[3].value:
  #          mouse.move(x=4)
   #     if not buttons[4].value:
   #         mouse.click(Mouse.LEFT_BUTTON)
    #        sleep(0.2)
   #     if not buttons[5].value:
   #         mouse.click(Mouse.RIGHT_BUTTON)
   #         sleep(0.2)

 #   if mode == 5:
  #      if not buttons[0].value:
 #           mediacontrol.send(ConsumerControlCode.VOLUME_INCREMENT)
  #          debounce()
  #      if not buttons[2].value:
  #          mediacontrol.send(ConsumerControlCode.VOLUME_DECREMENT)
  #          debounce()
  #      if not buttons[1].value:
  #          mediacontrol.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
  #          debounce()
  #      if not buttons[3].value:
  #          mediacontrol.send(ConsumerControlCode.SCAN_NEXT_TRACK)
  #          debounce()
  #      if not buttons[4].value:
  #          mediacontrol.send(ConsumerControlCode.PLAY_PAUSE)
  #          debounce()
  #      if not buttons[5].value:
  #          mediacontrol.send(ConsumerControlCode.STOP)
  #          debounce()
  #      if not buttons[9].value:
  #          mediacontrol.send(ConsumerControlCode.MUTE)
  #          debounce()

