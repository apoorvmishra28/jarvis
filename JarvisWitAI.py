import speech_recognition as sr
import pyttsx3
import os
import webbrowser as wb
from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib
# from skpy import Skype
import pyaudio
import wave
from wit import Wit



access_token = 'BQ6IG2ZLIRZU53D76IPPB5MFUVNOJDPT'
client = Wit(access_token=access_token)
spch = sr.Recognizer()

# skype = Skype('apoorv.m@cisinlabs.com','dhx3BNsdcV')

try:
    t_to_s_engine = pyttsx3.init()
except ImportError:
    print("Requested driver not found")
except RuntimeError:
    print("Driver failed to initialize")

voices = t_to_s_engine.getProperty('voices')
# return list of installed voices.
'''
afrikaans
aragonese
bulgarian
bosnian
catalan
czech
welsh
danish
german
greek
default
english
en-scottish
english-north
english_rp
english_wmids
english-us
en-westindies
esperanto
spanish
spanish-latin-am
estonian
persian
persian-pinglish
finnish
french-Belgium
french
irish-gaeilge
greek-ancient
hindi
croatian
hungarian
armenian
armenian-west
indonesian
icelandic
italian
lojban
georgian
kannada
kurdish
latin
lingua_franca_nova
lithuanian
latvian
macedonian
malayalam
malay
nepali
dutch
norwegian
punjabi
polish
brazil
portugal
romanian
russian
slovak
albanian
serbian
swedish
swahili-test
tamil
turkish
vietnam
vietnam_hue
vietnam_sgn
Mandarin
cantonese
'''
####################################################################################################
# for voice in voices:
#     print(voice.id)

t_to_s_engine.setProperty('voice', 'default')
rate = t_to_s_engine.getProperty('rate')
new_voice_rate = 130
t_to_s_engine.setProperty('rate',new_voice_rate)

# t_to_s_engine.say('Hello Sir, this is Jarvis.')
# t_to_s_engine.runAndWait() # this function runs executes the program and wait till
# the sentence is completely executed.


def speak_text_cmd(cmd):
    # this function is to get the reply from Jarvis
    t_to_s_engine.say(cmd)
    t_to_s_engine.runAndWait()


def feed_voice_cmd():
    # Read users voice command
    voice_text = ''
    print('Listening....')
    # import pdb; pdb.set_trace()
    with sr.Microphone() as source:
        spch.adjust_for_ambient_noise(source, duration=1)
        spch.energy_threshold += 280
        audio = spch.listen(source)

    try:
        response = client.speech()
        voice_text = sr.recognize_google(audio)
        print('You said {}'.format(response))
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("Network Error." + str(e))

    return  response


if __name__ == '__main__':
    speak_text_cmd('Hello Sir, This is Jarvis, your Artificial Intelligence.')

    while True:
        voice_note = feed_voice_cmd()
        chrome = '/usr/bin/firefox'
        print('cmd :{}'.format(voice_note))
        #####################################  Greetings  ###########################################
        if 'hello' in voice_note:
            speak_text_cmd('Hello Sir. How can I help you')
            continue
        ####################################  Open Youtube  #########################################
        if ('open youtube' or 'youtube') in voice_note:
            url = 'https://www.youtube.com/'
            wb.get(chrome).open(url)
            continue
        #################################  Play Youtube videos  #####################################
        if 'play' in voice_note:
            length = voice_note.find('play') + len('play') + 1
            q = voice_note[length:]
            url = 'https://www.youtube.com/results?search_query=' + q
            response = urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html)
            vid = soup.findAll(attrs={'class':'yt-uix-tile-link'})
            # import pdb; pdb.set_trace()
            video = vid[0]
            url = "https://www.youtube.com" + video['href']
            wb.get(chrome).open(url)
            continue
        #######################################  Skype  #############################################
        # if 'skype' in voice_note:
        #     length = voice_note.find('to') + len('to') + 1
        #     name = voice_note[length:]
        #     chats = skype.contacts[name].chat
        #     speak_text_cmd('Speak the message you want to send to {} on skype'.format(name))
        #     message = feed_voice_cmd()
        #     m_length = message.find('send') + len('send') + 1 # message length
        #     main_msg = message[m_length:]
        #     chats.sendMsg(main_msg)
        #     continue
        #######################################  Email  #############################################
        if 'email' in voice_note:
            speak_text_cmd('Who is the recipient ?')
            recipient = feed_voice_cmd()
            speak_text_cmd('What\'s {} email address ?'.format(recipient))
            recipient_email = feed_voice_cmd()
            print(recipient_email)
            speak_text_cmd('What\'s the email subject ?')
            subject = feed_voice_cmd()
            print(subject)
            speak_text_cmd('What\'s the content of the email ?')
            body_content = feed_voice_cmd()
            #### mail setup ####
            message = 'Subject: {}\n\n {}'.format(subject, body_content)
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            #### identify to serve ####
            mail.ehlo()
            ### encrypt ###
            mail.starttls()
            mail.login('jai.s@cisinlabs.com', 'gLNfrecfg0')
            fromadr = 'jai.s@cisinlabs.com'
            ### send mail ###
            mail.sendmail(fromadr, recipient_email, message)
            ### close connection ###
            mail.close()
            speak_text_cmd('email sent.')
            continue

        ########################################  Exit  #############################################
        if 'exit' in voice_note:
            speak_text_cmd('Bye Sir. See you soon.')
            exit()