import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from tkinter import messagebox
from tkinter import font
import tkinter as tk
import pygame
import time
import json
import sys

pygame.mixer.init()

from __init__ import main_window, driver

def cleanup():
    '''
    Clean up function when application is closed. 
    Closes browser 
    '''
    driver.quit()
    return


def success_chime():
    pygame.mixer.music.load('./assets/success_chime.mp3')
    pygame.mixer.music.play()

def play_pop():
    pygame.mixer.music.load('./assets/pop.mp3')
    pygame.mixer.music.play()

def play_error():
    pygame.mixer.music.load('./assets/error.mp3')
    pygame.mixer.music.play()

def show_popup(message, error=False):
    if error:
        play_error()
    else:
        play_pop()
    popup = tk.Toplevel()
    popup.title("Action Required")

    # Custom size of the pop-up window
    window_width = 300
    window_height = 200
    
    # Calculate the center position of the screen
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x_coordinate =  (screen_width - window_width) - ((screen_width - window_width) // 8 )
    y_coordinate = ((screen_height - window_height) // 8)

    # Set the window location and size
    popup.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    popup.attributes("-topmost", True)

    header = tk.Label(popup, text='ALERT:', wraplength=250, font=font.Font(weight="bold"), foreground="red")
    label = tk.Label(popup, text=message, wraplength=250, font=font.Font(weight="bold"))
    continue_button = tk.Button(popup, text="CONTINUE", command=popup.destroy, cursor="pointinghand")

    header.pack(side="top", pady=10)
    label.pack(side="top", pady=10)  
    continue_button.pack(side="top", pady=10) 
    popup.wait_window()
    popup.update()

def submit_input(input_popup, entry, input_var):
    input_text = entry.get()
    input_var.set(input_text)
    input_popup.destroy()

def show_input_popup(title, message, password=False):
    play_pop()
    input_popup = tk.Toplevel()
    input_popup.title(title)

    # Custom size of the pop-up window
    window_width = 300
    window_height = 200
    
    # Calculate the center position of the screen
    screen_width = input_popup.winfo_screenwidth()
    screen_height = input_popup.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2

    input_popup.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    input_popup.attributes("-topmost", True)

    label = tk.Label(input_popup, text=message, wraplength=250, font=font.Font(weight="bold"))
    label.pack(pady=20)

    input_var = tk.StringVar()

    entry = tk.Entry(input_popup, textvariable=input_var, show="*" if password else "")
    entry.pack()
    entry.focus_set()
    entry.bind("<Return>", lambda event: submit_input(input_popup, entry, input_var))
    #entry.bind("<Return>", lambda event: submit_input(input_popup, entry))

    input_popup.wait_window()
    input_popup.update()
    return input_var.get().strip()

def load_config():
    try:
        # Load JSON from a file
        with open('./config.json', 'r') as file:
            config = json.load(file)
        return config
    except:
        USERNAME = show_input_popup(title="Login to LinkedIn", message='Enter login email:')
        #USERNAME = input_text.strip()
        time.sleep(1)
        PASSWORD = show_input_popup(title="Login to LinkedIn", message='Enter password:')
        time.sleep(1)

        config = {
            "Email": USERNAME,
            "Password": PASSWORD
        }

        # Write dictionary to a JSON file
        with open('./config.json', 'w') as file:
            json.dump(config, file, indent=4)
        return config