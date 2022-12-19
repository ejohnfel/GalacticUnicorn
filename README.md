# GalacticUnicorn
Modified code for my Pimoroni Galactic Unicorn LED Panel

I heavily modified the main.py module, and updated the remaining modules that come with the default install so that they exit and go back to main instead of reset the device. The main.py no longer resets the device and has a try-except block to catch any errors and display an error message before halting.

This change was made to allow for selecting through the buttons with state and to be sure any bad code did not brick the display. It's not perfect, but it should catch most things.

Also added a function, msg.py to display messages based on an internal array of strings to display.

Lastly, button changes.

Button A : displays the messages in the selected array. There is an if-elfi-else structure to fill out the array for messages and a variable Panel which can be used to select which block of messages to display. The panel variable is an integer, unrecognized numbers simply display's test messages. This change is in case you have multiple displays that you may want to have multiple, separate, messages on. Keep clicking the button to cycle through the messages.

Button B : compacts all the effects (fire, retroprompt, supercomputer, rainbow) to this button, while adding some new effects to fire and supercomputer. Keep clicking the button to cycle through the effects.

Button C : shows holiday messages. Keep clicking the button to cycle through the messages.

Button D : Halts the Display (useful for when some code goes wrong on the microcontroller).

Sleep, lux+, lux- and reset work as normal.
