"""
As with all stupid projects I do, I must preface with "I am not responsible for whatever stupid thing you decide to do with this program".
Basically what it does is it flashbangs the living daylights out of you.
It's also highly customisable.
At some point I'll make a tkinter interface to go with this, I don't know.
Also I comment a lot because I know you coders really like documentation but don't like doing it
"""

import os
"""
Annoying bit of note: pygame (yes, a library) prints out a dumb prompt that advertises itself
so I hid it for you; have fun with this information and whatever because it's wreaked havoc
on some other projects
"""
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import pyautogui
import numpy as np
import time
import tkinter as tk #note-to-self: I need to 
import threading
import sys

# ---------------
"""
I'm making this bit super clear for you so you can customise and make your prank so much worse or more forgiving:
BRIGHTNESS_THRESHOLD (0 for black, 255 for white): when brightness go below threshold, flashbang
    + Normally I put 90 to punish dark mode users
    + But if you are seriously twisted just raise it up. To each their own...
CHECK_INTERVAL (seconds until the next time we find the average brightness)
    + Original settings: 5 seconds.
AUDIO_FILE (obviously the audio file)
    + You can get the flashbang.mp3 file also from my Github; however this can be replaced with something else
    + Who's stopping you from rickrolling people in the big '26? Nobody.
whyNotDeleteMyself (True/False): Deletes self, along with any traces of the flashbang program if True.
SLEEPER (seconds): How long you want to give yourself time to run from the machine before it flashbangs your victim.
    + This trick is only funny once in public. Trust me, I've tried it. Give yourself ample time to run.
"""
BRIGHTNESS_THRESHOLD = 90
CHECK_INTERVAL = 5
AUDIO_FILE = "flashbang.mp3" #Note: You have to load the sound into the same folder as this thing
                             #unless I'm brain dead enough to be making an .exe file of flashbang
whyNotDeleteMyself = False
SLEEPER = 20 #You can modify this to 3 seconds if you want to debug, 20 to run very far
#---------------

# Optional debugging variable. Off by default since it will print to console the program's path
# I don't think this will be useful to myself anymore
debug = False 


def avg_brightness(samples=30): #Samples a ton of places on the screen and determines how bright it is
    width, height = pyautogui.size()
    screenshot = pyautogui.screenshot()
    total_brightness = 0
    for _ in range(samples):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        color = screenshot.getpixel((x, y))
        total_brightness += sum(color) / 3
    return total_brightness / samples

def play_sound(): #plays the sound
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(AUDIO_FILE)
        pygame.mixer.music.play()
    except:
        exit() # We want this thing to be as godsdamned discreet as possible so
               # I'll accept a quiet exit if the prank fails because you forgot
               # to load the audio file in

def flashbang():
    # I mean you can just take this flashbang code but credit me if you do
    threading.Thread(target=play_sound, daemon=True).start()
    fWindow = tk.Tk()
    fWindow.configure(bg="white")
    fWindow.attributes('-fullscreen', True)
    fWindow.attributes('-alpha', 0.0) #The window is fully transparent initially

    """
    I cannot actually believe that tkinter does not do popup windows unless I specify it to
    so here's the code to front a window, which in this case I'll be making the white flashbang appear with
    """
    fWindow.attributes('-topmost', 1)
    fWindow.update()
    fWindow.attributes('-topmost', 0)

    def fade(window, start_alpha, end_alpha, steps=50, duration=1.5):
    # Fades in/out a tkinter window slowly (like a post-flashbang thing)
        step = (end_alpha - start_alpha) / steps
        delay = duration / steps
        alpha = start_alpha
        for _ in range(steps):
            alpha += step
            window.attributes('-alpha', alpha)
            window.update()
            time.sleep(delay)

    # What it should do is fade in with a massive speed ramp, then slowly fade out
    # Also please note that the flashbang currently lasts 3.5 seconds something, including sound.
    # So if you're planning on importing other audio you may have to plan something out
    fade(fWindow, 0.0, 1.0, steps=20, duration=0.01)
    time.sleep(0.5)
    fade(fWindow, 1.0, 0.0, steps=100, duration=3)
    fWindow.destroy()



while True:
    brightness = avg_brightness()
    if debug: print(f"Brightness: {brightness:.1f}")
    
    if brightness < BRIGHTNESS_THRESHOLD:
        time.sleep(SLEEPER) #As soon as the program is set up in the correct way, RUN. JUST RUN GODSDAMNED IT.
        flashbang()
        break
    time.sleep(CHECK_INTERVAL) #Should check every few seconds or so.
    #I'm not sure if decreasing the interval makes it require more resources and give the prank away?




"""
This bit is the self-destruct button, basically.
Oh, and if you plan to do any sort of modification, please for goodness sake keep a second copy of this thing
I cannot tell you how many times people asked me "so do I just fish the file out of the trash folder" erm
 no mate rm -f does not work that way. 
"""
script_path = os.path.realpath(sys.argv[0])
audio_path = os.path.join(os.path.dirname(script_path), AUDIO_FILE)
try:
    # Turns out you need to stop the sound from playing to remove lock on file
    # This actually caused a ton of anguish across a couple hours
    pygame.mixer.music.stop()
    pygame.mixer.quit()
except Exception:
    pass
time.sleep(2)

if whyNotDeleteMyself:
    if debug:
        if os.path.exists(audio_path): print(f"Deleting {audio_path}")
        if os.path.exists(script_path): print(f"Deleting {script_path}")

    # Be very careful when modding this bit.
    if os.name == "nt":
        # Terrify the heck out of your favourite Windows user!
        os.system(f'ping localhost -n 3 >nul && del "{audio_path}" && del "{script_path}"')
    else:
        # Also should work on other OS that uses bash
        os.system(f'sleep 2 && rm -f "{audio_path}" "{script_path}"')
elif debug:
    print(f"Would delete:\n  {script_path}\n  {audio_path}. Please keep a second copy of your file in case you forget.")
