import pyttsx3
import os
import webbrowser as wb
from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib
import speech_recognition as sr
from recordStream import record_audio, read_audio
from weather import Weather, Unit
import geocoder

access_token = 'BQ6IG2ZLIRZU53D76IPPB5MFUVNOJDPT'
# client = Wit(access_token=access_token)

spch = sr.Recognizer()
# skype = Skype('apoorv.m@cisinlabs.com','dhx3BNsdcV')

# import pdb; pdb.set_trace()
# print(g.latlng)

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
    # voice_text = ''
    response = ''
    print('Listening....')

    with sr.Microphone() as source:
        spch.adjust_for_ambient_noise(source, duration=1)
        spch.energy_threshold += 280
        audio = spch.listen(source)

    try:
        response = spch.recognize_google(audio) #, key='BQ6IG2ZLIRZU53D76IPPB5MFUVNOJDPT')
        print('You said :-> {}'.format(response))
    except  sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("Network Error." + str(e))
    # response = client.speech(voice_text, None, { 'Content-Type' : 'audio/wav' })
    # # voice_text = sr.recognize_google(audio)
    # print('You said {}'.format(response['_text']))

    return  response #['_text']

def send_email():
    speak_text_cmd('Who is the recipient ?')
    recipient = feed_voice_cmd()
    speak_text_cmd('What\'s {} email address ?'.format(recipient))
    recipient_email = feed_voice_cmd()
    recipient_email = recipient_email.lower().replace(' ', '')
    return recipient_email

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
        if ('open YouTube' or 'YouTube') in voice_note:
            url = 'https://www.youtube.com/'
            wb.get(chrome).open(url)
            continue
        #################################  Play Youtube videos  #####################################
        if 'play' in voice_note:
            length = voice_note.find('play') + len('play') + 1
            q = voice_note[length:]
            q = q.replace(' ', '+').lower()
            url = 'https://www.youtube.com/results?search_query=' + q
            # import pdb; pdb.set_trace()
            response = urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html)
            vid = soup.findAll(attrs={'class':'yt-uix-tile-link'})
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
            speak_text_cmd('@')
            recipient_email = send_email()
            if '.com' and '@' in recipient_email:
                pass
            else:
                speak_text_cmd('Please give valid email address')
                recipient_email = send_email()

            speak_text_cmd('What\'s the email subject ?')
            subject = feed_voice_cmd()
            # if '8' or 'at' in subject:
            #     pass
            print(subject)
            # import pdb; pdb.set_trace()
            speak_text_cmd('Add greatings')
            greetings = feed_voice_cmd()
            print(greetings)
            speak_text_cmd('What\'s the content of the email ?')
            body_content = feed_voice_cmd()
            #### mail setup ####
            message = 'Subject: {}\n\n {} \n\n {}'.format(subject, greetings, body_content)
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
            speak_text_cmd('What else you want me to do.')
            continue

        #####################################  Temperature   ########################################

        if 'temperature' in voice_note:
            weather = Weather(unit=Unit.CELSIUS)
            g = geocoder.ip('me')
            lookup = weather.lookup_by_latlng(g.lat, g.lng)
            condition = lookup.condition
            print(condition.temp)
            speak_text_cmd("The day is {} and the temperature is {}".format(condition.text, condition.temp))
            continue

        ########################################  Exit  #############################################
        if 'exit' in voice_note:
            speak_text_cmd('Bye Sir. See you soon.')
            exit()