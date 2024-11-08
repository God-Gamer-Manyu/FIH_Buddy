#from openai import OpenAI
import threading
from threading import Thread

import openai
from dotenv import load_dotenv
import os
import datetime
import customtkinter
import tkinter
from PIL import ImageTk, Image
import concurrent.futures
import time
import pyttsx3

import Utility
from Capture import Capture
from Utility import SoundManager

# Global variables
# Fonts
FONT = Utility.FONT
# stored files
IMAGES = Utility.IMAGES
# Sound effects
SOUND_EFFECTS = Utility.SOUND_EFFECTS
# adjustment variables
MESSAGE_LINE_LENGTH = 48
PIX_LINE = 15
BORDER_PIX = 44
CLAMP_LEN = 350

load_dotenv()

# todo: remove
openai.api_key = os.getenv("OPEN_AI_API_KEY")
assistant_id = os.getenv("OPEN_AI_ASSIST_ID")
WHISPER_CLIENT = openai.OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
#WHISPER_CLIENT = openai.OpenAI(api_key="")


# method which gets the output from open AI
def ask_openai(prompt):
    try:
        def create_thread(ass_id, prompt):
            # create a thread
            thread = openai.beta.threads.create()
            my_thread_id = thread.id
            # create a message
            message = openai.beta.threads.messages.create(
                thread_id=my_thread_id,
                role="user",
                content=prompt
            )
            # run
            run = openai.beta.threads.runs.create(
                thread_id=my_thread_id,
                assistant_id=ass_id,
            )
            return run.id, thread.id

        def check_status(run_id, thread_id):
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id,
            )
            return run.status

        my_run_id, my_thread_id = create_thread(assistant_id, prompt)
        status = check_status(my_run_id, my_thread_id)
        while status != "completed":
            status = check_status(my_run_id, my_thread_id)
            time.sleep(0.1)
        response = openai.beta.threads.messages.list(
            thread_id=my_thread_id
        )
        if response.data:
            return response.data[0].content[0].text.value
    except Exception as e:
        raise Exception(str(e))


class AiChat:
    def __init__(self, history):
        if not history:
            self.history = [('Hello, who are you?',
                             "Hi I am your friendly neighbourhood FIH buddy. I'm here to help you with your Foundation of Indian Heritage queries. How can I help you?",
                             str(datetime.datetime.now()))]
        else:
            self.history = history

    def chatgpt_clone(self, message):
        s = []  # storing history as one list
        for i in self.history:  # adding the history
            s.append(i[0])
            s.append(i[1])
        print(s)
        s.append('\n' + message)  # for creation of string
        inp = ' '.join(s)  # string to send to open AI
        try:
            output = ask_openai(inp)  # getting the output
        except Exception as e:
            print(e)
            return [('', 'Error while connecting to the internet, please check your internet connection')]
        self.history.append((message, '\n' + output, str(datetime.datetime.now())))  # updating the history
        return self.history  # returning the whole history

    def mainloop(self, app, size_x, size_y, profile_address, username, conversation, password):
        customtkinter.set_appearance_mode('dark')  # set mode
        customtkinter.set_default_color_theme('dark-blue')  # set theme

        app.geometry(f'{size_x}x{size_y}')  # Set screen size
        app.title("FIH Buddy")  # Set title
        # set the icon for the window
        app.iconbitmap(IMAGES['logo_ico'])
        app.wm_iconbitmap(IMAGES['logo_ico'])

        def close_window():
            #Main.Main.save_login_cred(username, password, profile_address)
            Utility.SoundManager.quit()
            app.destroy()

        app.protocol("WM_DELETE_WINDOW", close_window)

        # BG
        bg_img = ImageTk.PhotoImage(Image.open(IMAGES['bg']))
        # noinspection PyTypeChecker
        bg_l1 = customtkinter.CTkLabel(master=app, image=bg_img, text='')
        bg_l1.pack()

        # TODO: Make ui grid and make them scalable
        # Main placeholder
        frame = customtkinter.CTkFrame(master=bg_l1, width=size_x - 50, height=size_y - 50, corner_radius=15)
        frame.place(relx=.5, rely=.5, anchor=tkinter.CENTER)

        # back method
        def back():
            pass
            #bg_l1.destroy()
            #main = Main.Main(username, conversation, password, profile_address, self.history)
            #main.run(app)

        # back button
        #back_btn = customtkinter.CTkButton(master=bg_l1, width=30, height=30, text='Back', font=FONT['Comic'],
        #                                   command=back)
        #back_btn.place(x=45, y=15, anchor=tkinter.CENTER)

        # input field
        txt_field = customtkinter.CTkEntry(master=frame, width=size_x - 170, placeholder_text='Type Here',
                                           font=FONT['Comic'])
        txt_field.place(x=25, y=size_y - 100)

        def mic_on_off():
            mic_btn.configure(state=customtkinter.DISABLED)
            mic_obj = Capture()
            mic_obj.adjust_time(10)
            mic_obj.get_audio()
            mic_btn.configure(state=customtkinter.NORMAL)

            audio_file = open("Resources/Audio_Recordings/speech.wav", "rb")
            transcript = WHISPER_CLIENT.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

            txt_field.delete(0, tkinter.END)  # clearing input field
            txt_field.insert(tkinter.END, transcript.text)
            SoundManager.play(SOUND_EFFECTS['mic_off'])
            mic_btn.configure(state=customtkinter.NORMAL)
            enter_btn()

        # Todo: do space microphone
        #is_mic_on = False
        # def mic_on_off_space(event=None):
        #     is_mic_on
        #     if not is_mic_on:
        #         print('mic on')
        #         is_mic_on = True
        #     pass
        #
        # def mic_on_off_space_release(event=None):
        #     print('mic off')
        #     pass



        # microphone
        mic_img = customtkinter.CTkImage(Image.open(IMAGES['mic']))
        mic_btn = customtkinter.CTkButton(master=frame, width=30, corner_radius=5, command=mic_on_off, text='', hover_color='red',
                                        image=mic_img)
        mic_btn.place(x=size_x - 140, y=size_y - 100)

        # Todo: do space microphone
        # app.bind('<space>', mic_on_off_space)  # Space  button function
        # app.bind('<KeyRelease-space>', mic_on_off_space_release)  # Enter button function

        # message holder
        message_area = customtkinter.CTkScrollableFrame(master=frame, width=size_x - 115, height=size_y - 135)
        message_area.place(x=25, y=15)

        # User message template
        class User:

            def __init__(self, message):
                self.message = message

            def size_h(self):  # Determines the relative size of message widget
                # Adjustment values
                pix_line = PIX_LINE
                border_pix = BORDER_PIX

                # message
                mes = self.message
                mes = mes.split('\n')

                # finding length
                max_len = max(list(map(len, mes)))
                if max_len >= MESSAGE_LINE_LENGTH:
                    mes_len = CLAMP_LEN
                else:
                    mes_len = max_len % MESSAGE_LINE_LENGTH
                mes_len = (mes_len * 7) + 10

                def clamp(value, min_value, max_value):
                    return max(min(value, max_value), min_value)

                mes_len = clamp(mes_len, 50, CLAMP_LEN)

                # finding the height
                height = len(mes)
                for j in mes:
                    length = len(j) / MESSAGE_LINE_LENGTH
                    if length > 1:
                        height += int(length)
                height *= pix_line
                if height == 15:
                    return 34, mes_len

                return height + border_pix, mes_len

            def draw(self, current_time=''):
                Utility.SoundManager.play(SOUND_EFFECTS['send'])
                mes_h, mes_y = self.size_h()  # Getting the desired height

                # message holder
                us_mes = customtkinter.CTkFrame(master=message_area, width=mes_y + 45, height=mes_h + 30,
                                                border_width=1)
                us_mes.pack(anchor='e')
                message_area.focus = us_mes
                #us_mes.focus_set()
                # display message
                us_txt = customtkinter.CTkTextbox(master=us_mes, width=mes_y, height=mes_h, font=FONT['Comic'],
                                                  corner_radius=7, border_spacing=1)
                us_txt.insert(customtkinter.END, text=self.message)
                us_txt.place(x=5, y=5)
                us_txt.configure(state=customtkinter.DISABLED)

                # display profile pic
                us_img = customtkinter.CTkImage(Image.open(profile_address))
                us_img_l = customtkinter.CTkLabel(master=us_mes, image=us_img, width=30, height=30, text='')
                us_img_l.place(x=mes_y + 5, y=5)

                # display current_time stamp
                if current_time == '':
                    current_time = datetime.datetime.now()
                us_time = customtkinter.CTkLabel(master=us_mes, text=str(current_time)[:-10], width=30,
                                                 height=10, font=FONT['t_stamp'])
                us_time.place(x=mes_y - 30, y=mes_h + 12)

        # AI message template
        class Ai:

            @staticmethod  # Determines the relative size of message widget
            def size_h(message):
                # adjustments
                pix_line = PIX_LINE
                border_pix = BORDER_PIX

                # message
                mes = message
                mes = mes.split('\n')

                # finding relative length
                max_len = max(list(map(len, mes)))
                if max_len >= MESSAGE_LINE_LENGTH:
                    mes_len = CLAMP_LEN
                else:
                    mes_len = max_len % MESSAGE_LINE_LENGTH
                mes_len = (mes_len * 7) + 10

                def clamp(value, min_value, max_value):
                    return max(min(value, max_value), min_value)

                mes_len = clamp(mes_len, 50, CLAMP_LEN)

                # finding relative height
                height = len(mes)
                for j in mes:
                    length = len(j) / MESSAGE_LINE_LENGTH
                    if length > 1:
                        height += int(length)
                height *= pix_line
                if height == 15:
                    return 34, mes_len
                return height + border_pix, mes_len

            def draw_from_ques(self, question, history):
                mes_h, mes_y = self.size_h('.....')
                # message placeholder
                client_mes = customtkinter.CTkFrame(master=message_area, width=mes_y + 45, height=mes_h + 30,
                                                    border_width=1)
                client_mes.pack(anchor='w')

                # bot logo
                client_img = customtkinter.CTkImage(Image.open(IMAGES['bot']))
                client_img_l = customtkinter.CTkLabel(master=client_mes, image=client_img, width=30, height=30,
                                                      text='')
                client_img_l.place(x=5, y=5)

                # timestamp
                cur_time = datetime.datetime.now()
                client_time = customtkinter.CTkLabel(master=client_mes, text=str(cur_time)[:-10],
                                                     width=30,
                                                     height=10, font=FONT['t_stamp'])
                client_time.place(x=mes_y - 30, y=mes_h + 12)
                # bot message
                client_txt = customtkinter.CTkTextbox(master=client_mes, width=mes_y, height=mes_h,
                                                      font=FONT['Comic'],
                                                      corner_radius=7,
                                                      border_spacing=1)
                client_txt.insert(customtkinter.END, text='')
                client_txt.place(x=35, y=5)

                task_finished = False

                def update_text():
                    if not task_finished:
                        # delete all existing text
                        client_txt.delete('1.0', customtkinter.END)
                        # insert the current message and dots
                        dots = ''

                        for ct in range(5):
                            dots += '.'
                            client_txt.delete('1.0', customtkinter.END)
                            client_txt.insert(customtkinter.END, dots)
                            app.update()
                            time.sleep(.2)

                        # schedule the next update
                        app.after(250, update_text)

                # Create a thread pool executor with one worker thread
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    # Submit the function to the executor and get a Future object
                    aichat = AiChat(history)
                    future = executor.submit(aichat.chatgpt_clone, question)

                    # Do other things while the function is running in another thread
                    update_text()

                    # Get the return value of the function (this blocks until the function completes)
                    response = future.result()[-1][1]  # retrieving bot output
                    task_finished = True
                    Utility.SoundManager.play(SOUND_EFFECTS['receive'])
                    client_txt.configure(state=customtkinter.DISABLED)

                # refining output
                res = ''
                let = False
                for resp in response:
                    if resp in ' ?.,\n' and not let:
                        continue
                    if resp.isalnum():
                        res += resp
                        let = True
                        continue
                    else:
                        res += resp

                mes_h, mes_y = self.size_h(res)  # getting relative height
                client_mes.destroy()
                client_time.destroy()
                client_txt.destroy()

                # message placeholder
                client_mes = customtkinter.CTkFrame(master=message_area, width=mes_y + 45, height=mes_h + 30,
                                                    border_width=1)
                client_mes.pack(anchor='w')

                # bot logo
                client_img = customtkinter.CTkImage(Image.open(IMAGES['bot']))
                client_img_l = customtkinter.CTkLabel(master=client_mes, image=client_img, width=30, height=30, text='')
                client_img_l.place(x=5, y=5)

                # timestamp
                client_time = customtkinter.CTkLabel(master=client_mes, text=str(cur_time)[:-10],
                                                     width=30,
                                                     height=10, font=FONT['t_stamp'])
                client_time.place(x=mes_y - 35, y=mes_h + 12)

                # bot message
                client_txt = customtkinter.CTkTextbox(master=client_mes, width=mes_y, height=mes_h, font=FONT['Comic'],
                                                      corner_radius=7,
                                                      border_spacing=1)
                client_txt.insert(customtkinter.END, text=res)
                client_txt.configure(state=customtkinter.DISABLED)
                client_txt.place(x=35, y=5)

                def say(resp):
                    engine.say(resp)
                    engine.runAndWait()

                t1 = threading.Thread(target=say, args=(res,))
                t1.start()

            def draw(self, message, current_time):
                Utility.SoundManager.play(SOUND_EFFECTS['receive'])
                mes_h, mes_y = self.size_h(message)  # getting relative height

                # message placeholder
                client_mes = customtkinter.CTkFrame(master=message_area, width=mes_y + 45, height=mes_h + 30,
                                                    border_width=1)
                client_mes.pack(anchor='w')

                # bot logo
                client_img = customtkinter.CTkImage(Image.open(IMAGES['bot']))
                client_img_l = customtkinter.CTkLabel(master=client_mes, image=client_img, width=30, height=30, text='')
                client_img_l.place(x=5, y=5)

                # timestamp
                client_time = customtkinter.CTkLabel(master=client_mes, text=str(current_time)[:-10],
                                                     width=30,
                                                     height=10, font=FONT['t_stamp'])
                client_time.place(x=mes_y - 35, y=mes_h + 12)

                # bot message
                client_txt = customtkinter.CTkTextbox(master=client_mes, width=mes_y, height=mes_h, font=FONT['Comic'],
                                                      corner_radius=7,
                                                      border_spacing=1)
                client_txt.insert(customtkinter.END, text=message)
                client_txt.configure(state=customtkinter.DISABLED)
                client_txt.place(x=35, y=5)

        def enter_btn(event=None):  # functioned called when enter key or send button is pressed
            enter.configure(state=customtkinter.DISABLED)
            print(event)
            user_mes = User(txt_field.get())  # invoking user message template
            user_mes.draw()  # displaying user message template

            ai_mes = Ai()  # invoking AI message template
            mes = txt_field.get()
            txt_field.delete(0, tkinter.END)  # clearing input field
            ai_mes.draw_from_ques(mes, self.history)  # displaying AI message template
            enter.configure(state=customtkinter.NORMAL)

        # sent button
        enter_img = customtkinter.CTkImage(Image.open(IMAGES['send']))
        enter = customtkinter.CTkButton(master=frame, width=30, corner_radius=5, command=enter_btn, text='',
                                        image=enter_img)
        enter.place(x=size_x - 100, y=size_y - 100)

        app.bind('<Return>', enter_btn)  # Enter button function

        # initial message display
        i_mes_h, i_mes_y = 74, 1125
        # message placeholder
        i_client_mes = customtkinter.CTkFrame(master=message_area, width=i_mes_y + 45, height=i_mes_h + 30,
                                              border_width=1)
        i_client_mes.pack(anchor='w')

        # bot logo
        i_client_img = customtkinter.CTkImage(Image.open(IMAGES['bot']))
        i_client_img_l = customtkinter.CTkLabel(master=i_client_mes, image=i_client_img, width=30, height=30, text='')
        i_client_img_l.place(x=5, y=5)

        # timestamp
        i_client_time = customtkinter.CTkLabel(master=i_client_mes, text=str(self.history[0][2])[:-10], width=30,
                                               height=10, font=FONT['t_stamp'])
        i_client_time.place(x=i_mes_y - 35, y=i_mes_h + 12)
        # bot message
        i_client_txt = customtkinter.CTkTextbox(master=i_client_mes, width=i_mes_y, height=i_mes_h, font=FONT['Comic'],
                                                corner_radius=7, border_spacing=1)
        i_client_txt.insert(customtkinter.END, text=self.history[0][1].strip())
        i_client_txt.configure(state=customtkinter.DISABLED)
        i_client_txt.place(x=35, y=5)

        ai = Ai()
        for i in self.history[1:]:
            user = User(i[0])
            user.draw(i[2])
            ai.draw(i[1], i[2])

        app.mainloop()  # update display per frame


if __name__ == '__main__':
    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')

    root = customtkinter.CTk()  # initiate custom Tkinter

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    main = AiChat([])
    main.mainloop(root, 1000, 600, 'Resources/images/user.png', 'Rohan', '', 'password')
