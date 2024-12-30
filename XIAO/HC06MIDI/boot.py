"""JoystickXL standard boot.py."""

import usb_hid  # type: ignore (this is a CircuitPython built-in)
from joystick_xl.hid import create_joystick

# This will enable all of the standard CircuitPython USB HID devices along with a
# USB HID joystick.
usb_hid.enable(
    (
        usb_hid.Device.KEYBOARD,
        usb_hid.Device.MOUSE,
        usb_hid.Device.CONSUMER_CONTROL,
        create_joystick(axes=8, buttons=128, hats=4),
    )
)

## https://circuitpython-joystickxl.readthedocs.io/en/stable/start.html
# This will enable a joystick USB HID device.  All other standard CircuitPython USB HID
# devices (keyboard, mouse, consumer control) will be disabled.
#usb_hid.enable((create_joystick(axes=8, buttons=128, hats=4),))
