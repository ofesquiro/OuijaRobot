FROM python
WORKDIR /app
COPY . .
RUN apt upgrade
RUN apt update
RUN pip install speechRecognition
RUN apt install portaudio19-dev -y
RUN apt-get install python3-pyaudio
RUN pip install pyaudio
#RUN pip3 install pygame

CMD ["python", "src/test.py"]