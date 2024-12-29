from gpiozero import Button
from signal import pause

button = Button(27, bounce_time=0.1)

button.when_pressed = lambda: print("Button pressed!")
button.when_released = lambda: print("Button released!")

pause()
