import os
import threading

from pygame import mixer
# todo: comment document and fix light warnings
###################
import customtkinter as ctk
import CTkListbox
###################

mixer.init()  # initialize the mixer

# Sound effects
SOUND_EFFECTS = {
    "join": "Resources/Sound effects/User join.wav",
    "send": "Resources/Sound effects/send_message.wav",
    "receive": "Resources/Sound effects/receive message.wav",
    'mic_on': "Resources/Sound effects/PowerOn.wav",
    'mic_off': "Resources/Sound effects/PowerOff.wav"
}
# stored files
MEMORY = {
    'cons': 'Resources/Memory/cons.dat',
    'f_key': 'Resources/Memory/file_key.key',
    'u_name': 'Resources/Memory/u_name.dat'
}
# Images
IMAGES = {'favicon': 'Resources/images/favicon.ico',
          'logo_ico': 'Resources/images/Icon.ico',
          'logo_png': 'Resources/images/Logo.png',
          'pass hide': 'Resources/images/pass_hide.png',
          'pass show': 'Resources/images/pass_show.png',
          'pattern': 'Resources/images/pattern_Home.png',
          'bg': 'Resources/images/BG_2_image.jpg',
          'bot': 'Resources/images/bot.png',
          'send': 'Resources/images/send.png',
          'user': 'Resources/images/user.png',
          'mic': 'Resources/images/mic.png'
}
# Fonts
FONT = {
    "Comic": ("Comic Sans MS", 13),
    "t_stamp": ("Comic Sans MS", 8),
    "Oth_uname": ("Comic Sans MS", 16),
    'Button': ('Comic Sans MS', 25),
    'In_field': ('Comic Sans MS', 20),
    'error': ('Comic Sans MS', 15)
}


class SoundManager:
    @staticmethod
    def play(address):

        def playsound(ads):
            sound = mixer.Sound(ads)
            sound.play()

        p1 = threading.Thread(target=playsound, args=(address,))
        p1.start()

    @staticmethod
    def quit():
        mixer.quit()
