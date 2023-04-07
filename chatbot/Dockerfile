FROM python:3.10

WORKDIR /chatbot
RUN python -m pip install --upgrade pip
RUN python -m pip install numpy tensorflow fastapi uvicorn gTTS
RUN pip install -U nltk
RUN python -m nltk.downloader -q Russian wordnet omw-1.4 punkt stopwords

COPY . /chatbot                                                                                                                                                                                                       

EXPOSE 5200
CMD ["uvicorn", "Host:app", "--host", "0.0.0.0", "--port", "5200"]