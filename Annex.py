import datetime,subprocess,os,pyautogui,string,random
import pyttsx3
import speech_recognition as sr
import sounddevice
from scipy.io.wavfile import write
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import pyperclip
from ttkthemes import themed_tk as tkth
import tkinter.scrolledtext as scrolledtext
from functools import partial

class SpeakRecog:
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    # print(voices[].id)
    # print(voices)

    """ VOICE RATE"""
    rate = engine.getProperty('rate')               # getting details of current speaking rate
    # print(rate)
    engine.setProperty('rate', 180)                 # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')           #getting to know current volume level (min=0 and max=1)
    # print(volume)                                 #printing current volume level
    engine.setProperty('volume', 1.0)               # setting up volume level  between 0 and 1
    scrollable_text=None
    def STS(self,scrollable_text):
        '''This is scrollable text sette '''
        self.scrollable_text=scrollable_text
    def updating_ST(self,data):
        self.scrollable_text.configure(state='normal')
        self.scrollable_text.insert('end',data+'\n')
        self.scrollable_text.configure(state='disabled')
        self.scrollable_text.see('end')
        self.scrollable_text.update()
    def updating_ST_No_newline(self,data):
        self.scrollable_text.configure(state='normal')
        self.scrollable_text.insert('end',data)
        self.scrollable_text.configure(state='disabled')
        self.scrollable_text.see('end')
        self.scrollable_text.update()
    def scrollable_text_clearing(self):
        self.scrollable_text.configure(state='normal')
        self.scrollable_text.delete(1.0,'end')
        self.scrollable_text.configure(state='disabled')
        self.scrollable_text.update()
    def speak(self,audio):
        """It speaks the audio"""
        self.updating_ST(audio)
        self.engine.say(audio)
        # engine.save_to_file('Hello World', 'test.mp3')
        self.engine.runAndWait()
        # engine.stop()

    def nonPrintSpeak(self,audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def takeCommand(self):
        """It take microphone input from the user and return string"""
        recog=sr.Recognizer()
        # mic=Microphone()
        with sr.Microphone() as source:
            #r.adjust_for_ambient_noise(source)
            self.updating_ST("Listening...")
            recog.pause_threshold = 1
            # r.energy_threshold = 45.131829621150224
            # print(sr.Microphone.list_microphone_names())
            #print(r.energy_threshold)
            audio=recog.listen(source)
        try:
            self.updating_ST("Recognizing...")
            query= recog.recognize_google(audio)
            self.updating_ST(f"You: {query}\n")
        except Exception as e:
            # print(e)
            self.updating_ST("Say that again please...")
            return 'None'
        return query

class PasswordGenerator:
    def action(self,pswd):
        pyperclip.copy(pswd)
    def showpswd(self,data,pswd):
        root=tk.Toplevel()
        root.title("Password Generator")
        root.iconbitmap('PasswordGenerator.ico')
        style = ttk.Style()
        style.configure('W.TButton',font=('calibri', 10, 'bold'),foreground ='purple',borderwidth ='4',background="pink")
        root.geometry("320x80+540+270")
        # root.eval('tk::PlaceWindow . center')     #this only works for Tk() instance not for Toplevel() instance
        label1=ttk.Label(root,text=data,font=("comicsansms",9,'bold')).pack()
        button1=ttk.Button(root,text='Copy to clipboard',style = 'W.TButton',command=partial(self.action,pswd)).pack(pady=20)
        root.resizable(0,0)
        root.mainloop()
        del root
    def givePSWD(self,scrollable_text):
        SR=SpeakRecog()
        SR.STS(scrollable_text)
        SR.speak("What type of password you want?")
        SR.updating_ST("\nPassword Level we have:-\n\nPoor Level\nAverage Level\nStrong Level\n")
        while(True):
            query=SR.takeCommand().lower()
            if ('poor' in query):
                self.showpswd("Your Password is : "+"".join(random.sample(string.ascii_letters,7)),"".join(random.sample(string.ascii_letters,7)))
                break
            elif ('average' in query):
                self.showpswd("Your Password is : "+"".join(random.sample(string.ascii_letters+string.digits,10)),"".join(random.sample(string.ascii_letters+string.digits,10)))
                break
            elif ('strong' in query):
                self.showpswd("Your Password is : "+"".join(random.sample(string.ascii_letters+string.digits+string.punctuation,13)),"".join(random.sample(string.ascii_letters+string.digits+string.punctuation,13)))
                break
            else:
                SR.speak("Please say it again")
        del SR
        
class TextSpeech:
    def txtspk(self):
        SR=SpeakRecog()
        SR.nonPrintSpeak(self.text.get(1.0,tk.END))
        del SR
    def opentxt(self):
        self.root.focus_force()    
        try:
            file_path=filedialog.askopenfilename(initialdir =r"C:\Users\Vishal\Documents\Projects or important programs\jarvis\Notes",title="Select file",filetypes=(('text file',"*.txt"),("All files", "*.*")))
            with open(file_path,'r') as f:
                g=f.read()
        
            self.root.focus_force()    
            self.text.delete(1.0,tk.END)
            self.text.insert(tk.INSERT,g)
            self.text.update()
            SR=SpeakRecog()
            SR.nonPrintSpeak(g)
            del SR
        except FileNotFoundError as e:
            self.root.focus_force()    
            pass

    def __init__(self):
        self.root=tkth.ThemedTk()
        self.root.get_themes()
        self.root.set_theme("radiance")
        self.root.resizable(0,0)
        self.root.configure(background='white')
        self.root.title("Text to Speech")
        self.root.iconbitmap('text_to_speech.ico')
        #root widget
        self.text=scrolledtext.ScrolledText(self.root,width=30,height=10,wrap=tk.WORD,padx=10,pady=10,borderwidth=5,relief=tk.RIDGE)
        self.text.grid(row=0,columnspan=3)
        #buttons
        self.listen_btn=ttk.Button(self.root,text="Listen",width=7,command=self.txtspk).grid(row=2,column=0,ipadx=2)
        self.clear_btn=ttk.Button(self.root,text="Clear",width=7,command=lambda:self.text.delete(1.0,tk.END)).grid(row=2,column=1,ipadx=2)
        self.open_btn=ttk.Button(self.root,text="Open",width=7,command=self.opentxt).grid(row=2,column=2,ipadx=2)
        self.root.focus_set()
        self.root.mainloop()
    
class note:
    def Note(self,data):
        date=datetime.datetime.now()
        filename=str(date).replace(':','-')+'-note.txt'
        a=os.getcwd()
        if not os.path.exists('Notes'):
            os.mkdir('Notes')
        os.chdir(a+r'\Notes')
        with open(filename,'w') as f:
            f.write(data)
        subprocess.Popen(['notepad.exe',filename])
        os.chdir(a)

class screenshot:
    def takeSS(self):
        img_captured=pyautogui.screenshot()
        a=os.getcwd()
        if not os.path.exists("Screenshots"):
            os.mkdir("Screenshots")
        os.chdir(a+'\Screenshots')
        date=datetime.datetime.now()
        img_captured.save('screenshot-'+str(date).replace(':','-')+'.png')
        os.chdir(a)
  
class StonePaperScissor:
    def start(self,scrollable_text):
        SR=SpeakRecog()
        SR.STS(scrollable_text)
        list1=['stone','paper','scissor']
        while(True):
            SR.scrollable_text_clearing()
            SR.updating_ST("------------------------------------WELCOME-------------------------------------------")
            SR.speak("\n\nThis game contains 3 rounds, those who win maximum rounds will be winner of this game.")
            human_score=0
            computer_score=0
            i=0
            while(i<3):
                if i==2:
                    if(human_score>computer_score):
                        SR.speak("\nNo need of 3rd round because human's score is obviously greater thean computer's.\n")
                        break
                    elif(human_score<computer_score):
                        SR.speak("\nNo need of 3rd round because computer's score is obviously greater thean human's.\n")
                        break

                SR.updating_ST(87*"*")
                while(True):
                    SR.speak("Your choice please-")
                    user_ip=SR.takeCommand().lower()
                    if(('stone' in user_ip) or ('paper' in user_ip) or ('scissor' in user_ip) or ('cutter' in user_ip) or ('rock' in user_ip)):
                        if(user_ip=='cutter'):
                            user_ip='scissor'
                        if(user_ip=='rock'):
                            user_ip='stone'
                        break
                    else:
                        SR.speak("\nIt did not match with the option that we have. Please enter your choice again.")
                comp_ip=random.choice(list1)
                if(user_ip==comp_ip):
                    SR.speak("\nIt is a tie, so it is not considered as a round.\n")

                elif((user_ip=='stone' and comp_ip=='paper') or (user_ip=='paper' and comp_ip=='scissor') or (user_ip=='scissor' and comp_ip=='stone') ):
                    computer_score+=1
                    SR.speak("\nComputer win this round.\n")
                    SR.speak(f"\nComputre's choice was {comp_ip}.\n")
                    SR.updating_ST(87*"+")
                    i+=1
                elif((comp_ip=='stone' and user_ip=='paper') or (user_ip=='scissor' and comp_ip=='paper') or (user_ip=='stone' and comp_ip=='scissor')):
                    human_score+=1
                    SR.speak("\nHuman win this round.\n")
                    SR.speak(f"\nComputre's choice was {comp_ip}.\n")
                    SR.updating_ST(87*"+")
                    i+=1
            if(human_score==computer_score):
                SR.speak("\nIt is a tie.\n")
            elif(human_score>computer_score):
                SR.speak("\nHuman is the winner of this game.\n")    
            else:
                SR.speak("\nComputer is the winner of this game.\n")
            SR.updating_ST(87*"*")
            SR.speak('If you want repeat this game then say REPEAT.')
            decision=SR.takeCommand().lower()
            if('repeat' not in decision):
                SR.speak("Getting out of this game to main thread.")
                break

class VoiceRecorer:
    def Record(self,scrollable_text):
        SR=SpeakRecog()
        SR.STS(scrollable_text)
        SR.speak("This recording is of 10 seconds.")
        fs=44100
        second=10
        SR.updating_ST("Recording.....")
        record_voice=sounddevice.rec(int(second * fs),samplerate=fs,channels=2)
        sounddevice.wait()
        a=os.getcwd()
        if not os.path.exists("Recordings"):
            os.mkdir("Recordings")
        os.chdir(a+'\Recordings')
        write("Recording-"+str(datetime.datetime.now()).replace(':','-')+".wav",fs,record_voice)
        SR.speak("Voice is recorded in \'Recordings\' folder.")
        os.chdir(a)
        del SR