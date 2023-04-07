import datetime
import Model as bt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from nltk.corpus import stopwords
russian_stopwords = stopwords.words("russian")
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
import uvicorn
import hashlib
import sched, time
import requests


# uvicorn Host:app --host 0.0.0.0 --port 5200

#GLOBAL VAR
__ID = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\TokenEnums\\RHVoice\\Evgeniy-Rus'
__AUDIOPATH = 'audio/'

# Vocoder setings
#vocoder = sx.init()
#vocoder.setProperty('voice', __ID)
#vocoder.setProperty('rate', vocoder.getProperty('rate') - 35)

# Assistent setings
assistent = bt.NLPneural(model_name="loadfile/ChatModel")
tager = bt.NLPrecom(model_name="loadfile/TagModel")

# App setings
app = FastAPI()

#JSON package format
class Item(BaseModel):
    message: str


# Audio files cleaner
s = sched.scheduler(time.time, time.sleep)


def cleaner():
    s.enter(60*2, 1, cleaner)  # Перезапуск через 2 минуты
    time = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M:%S")
    print(f'[Event]: Удаление аудио файлов\nВремя: {time}')

    audiofiles = os.listdir(__AUDIOPATH)
    for i in audiofiles:
        os.remove(__AUDIOPATH+i)


# Work test request
@app.get('/')
def hello_world():
    return 'Work sucsf'

@app.get('/audio/', status_code=200)
def audio(audio: str):
    return FileResponse(__AUDIOPATH+audio)

#chat bot
@app.post('/bot')
def post_data(data: Item):
    bot_ans , ints = assistent.request(data.message)
    time = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M:%S:%f")

    hash = hashlib.md5(time.encode()).hexdigest()
    audiofile = __AUDIOPATH + hash + ".mp3"

    bot_ans_audio=gTTS(bot_ans, lang='ru')

    bot_ans_audio.save(audiofile)

    print(f"Время: {time}\nAudio file: {audiofile}\n"
          f"User: {data.message}\nBot: {bot_ans}\n")

    return {"message": bot_ans, "audio": hash+'.mp3', "ints": ints }

@app.post("/tag")
def post_tag(data: Item):
    tag = tager.predict_tag(data.message)
    #resp = requests.get('http://DB:5210/events/all_events_by_chat', params={'tag_names': tag})
    return {"tags": tag}

if __name__ == "__main__":
    uvicorn.run("Host:app", host="127.0.0.1", port=5200)