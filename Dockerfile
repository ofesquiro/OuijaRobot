FROM python
workdir /app
copy . .
RUN apt upgrade
RUN apt update
RUN pip3 install speechRecognition
RUN apt install portaudio19-dev -y
RUN apt-get install python3-pyaudio
RUN pip3 install pyaudio
RUN pip3 install pocketsphinx
RUN pip3 install pygame

CMD ["python", "src/test.py"]