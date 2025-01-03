from gpiozero import Button
from signal import pause
import subprocess
import os

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WOODEN_BOX_SCRIPT = os.path.join(SCRIPT_DIR, "wooden_box.py")

def adjust_volume_action(amount="10%-"):
    try:
        subprocess.run(["amixer", "set", "Master", amount], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error adjusting volume: {e}")

def toggle_play():
    try:
        subprocess.run(["python3", WOODEN_BOX_SCRIPT, "toggle"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error toggle play: {e}")

play_toggle = Button(26, bounce_time=0.1)
play_toggle.when_released = toggle_play
volume_down = Button(27, bounce_time=0.1)
volume_down.when_released = lambda: adjust_volume_action("10%-")
volume_up = Button(17, bounce_time=0.1)
volume_up.when_released = lambda: adjust_volume_action("10%+")

pause()
