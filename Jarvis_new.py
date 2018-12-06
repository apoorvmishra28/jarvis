import sys
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QAbstractButton
import speech_recognition as sr
# from wit import Wit

import pyttsx3
import webbrowser as wb

######################################   Image Button   #######################################
class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
###############################################################################################

######################################   Jarvis speak   #######################################
def speak_text_cmd(cmd):
    # this function is to get the reply from Jarvis

    t_to_s_engine.say(cmd)
    t_to_s_engine.runAndWait()
###############################################################################################

######################################   Command feed   #######################################
def feed_voice_cmd():
    # Read users voice command
    voice_text = ''
    print('Listening....')
    # import pdb; pdb.set_trace()
    with sr.Microphone() as source:
        speech.adjust_for_ambient_noise(source, duration=1)
        speech.energy_threshold += 500
        audio = speech.listen(source)
    try:
        voice_text = speech.recognize_google(audio)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("Network Error." + str(e))

    return  voice_text
###############################################################################################

######################################   Window Frame   #######################################
class AI_Frame(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Jarvis AI')
        btn = PicButton(QPixmap('download.png'), self)
        btn.move(110, 60)
        btn.resize(80, 80)
        btn.clicked.connect(self.StartJarvis)
        self.show()

    def StartJarvis(self):
        speak_text_cmd('Hello Sir, This is Jarvis, your Artificial Intelligence.')

        while True:
            voice_note = feed_voice_cmd()
            speak_text_cmd(voice_note)
            chrome = '/usr/bin/google-chrome'
            print('cmd :{}'.format(voice_note))
            if 'hello' in voice_note:
                speak_text_cmd('Hello Sir. How can I help you')
                continue
            if ('open youtube' or 'youtube') in voice_note:
                url = 'https://www.youtube.com/'
                wb.get(chrome).open(url)
                continue
            if 'search' in voice_note:
                length = voice_note.find('play') + len('play') + 1
                q = voice_note[length:]
                import pdb; pdb.set_trace()
                url = 'https://www.youtube.com/results?search_query=' + q
                # page = requests.get(url)
                # tree = html.fromstring(page.content)
                # buyers = tree.xpath('//*[@id="container"]')
                # vid = buyers.xpath('//*[@id="dismissable"]')
                # a = vid[0]
                # p = a.get("data-context-item-id")
                # wb.open("https://www.youtube.com/watch?v=" + p)
            if 'exit' in voice_note:
                speak_text_cmd('Bye Sir. See you soon.')
                exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    speech = sr.Recognizer()


    try:
        t_to_s_engine = pyttsx3.init()
    except ImportError:
        print("Requested driver not found")
    except RuntimeError:
        print("Driver failed to initialize")

    voices = t_to_s_engine.getProperty('voices')
    t_to_s_engine.setProperty('voice', 'english')
    rate = t_to_s_engine.getProperty('rate')
    new_voice_rate = 130
    t_to_s_engine.setProperty('rate', new_voice_rate)


    window = AI_Frame()
    sys.exit(app.exec_())