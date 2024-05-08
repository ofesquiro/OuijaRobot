FROM python
workdir /app
copy . .
RUN pip3 install speechRecognition
RUN apt update
RUN apt install portaudio19-dev -y
RUN apt-get install python3-pyaudio
RUN pip3 install pyaudio
RUN pip3 install pocketsphinx

CMD ["python", "src/inputDevice.py"]