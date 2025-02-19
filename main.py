import tkinter
from tkinter import filedialog
from tkinter.ttk import Progressbar
import customtkinter
import pygame
from PIL import Image, ImageTk
from threading import Thread
import time
import os
import subprocess  # Use FFmpeg directly

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")  

##### Tkinter setup ######
root = customtkinter.CTk()
root.title('Music Player')
root.geometry('400x480')

# Initialize pygame mixer
pygame.mixer.init()

current_song_path = None  
converted_wav_path = None  
song_name_label = None  


def get_album_cover():
    """Displays a default black album cover"""
    image1 = Image.new("RGB", (250, 250), "black")  
    image2 = image1.resize((250, 250))
    load = ImageTk.PhotoImage(image2)

    label1 = tkinter.Label(root, image=load)
    label1.image = load
    label1.place(relx=.19, rely=.06)


def update_song_name(song_path):
    """Updates the song title label"""
    global song_name_label

    if song_name_label:
        song_name_label.destroy()

    stripped_string = os.path.basename(song_path)[:-4]  
    song_name_label = tkinter.Label(root, text=stripped_string, bg='#222222', fg='white')
    song_name_label.place(relx=.4, rely=.6)


def progress():
    """Handles the progress bar update"""
    if current_song_path:
        song_length = pygame.mixer.Sound(current_song_path).get_length()
        for _ in range(int(song_length * 3)):
            time.sleep(0.4)
            progressbar.set(pygame.mixer.music.get_pos() / 1000000)


def threading_progress():
    """Runs progress bar in a separate thread"""
    t1 = Thread(target=progress)
    t1.start()


def convert_to_wav(file_path):
    """Converts any format to WAV using FFmpeg if needed"""
    global converted_wav_path

    if file_path.lower().endswith(".wav"):
        return file_path  

    wav_file = file_path.rsplit(".", 1)[0] + ".wav"  

    if not os.path.exists(wav_file):
        print(f"Converting {file_path} to WAV using FFmpeg...")
        subprocess.run(["ffmpeg", "-i", file_path, wav_file, "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    converted_wav_path = wav_file
    return wav_file


def play_music():
    """Plays the selected music file"""
    global current_song_path

    if not current_song_path:
        print("No song selected.")
        return

    try:
        converted_file = convert_to_wav(current_song_path)  
        pygame.mixer.init()  
        pygame.mixer.music.load(converted_file)  
        pygame.mixer.music.play()  
        pygame.mixer.music.set_volume(0.5)  

        print(f"Playing: {converted_file}")  

        threading_progress()
        get_album_cover()
        update_song_name(current_song_path)

    except pygame.error as e:
        print("Error playing file:", e)


def open_file():
    """Opens file dialog to choose a song from the laptop"""
    global current_song_path

    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac *.aac")])
    
    if file_path:
        current_song_path = file_path
        print("Selected file:", current_song_path)  
        play_music()  


def stop_music():
    """Stops the currently playing music"""
    pygame.mixer.music.stop()


def volume(value):
    """Adjusts volume"""
    pygame.mixer.music.set_volume(float(value))


# UI Buttons
play_button = customtkinter.CTkButton(master=root, text='Open & Play', command=open_file)
play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

stop_button = customtkinter.CTkButton(master=root, text='Stop', command=stop_music)
stop_button.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

slider = customtkinter.CTkSlider(master=root, from_=0, to=1, command=volume, width=210)
slider.place(relx=0.5, rely=0.82, anchor=tkinter.CENTER)

progressbar = customtkinter.CTkProgressBar(master=root, progress_color='#32a85a', width=250)
progressbar.place(relx=.5, rely=.89, anchor=tkinter.CENTER)

root.mainloop()
