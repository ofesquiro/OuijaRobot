FROM python
workdir /app
copy . .
RUN pip install speechRecognition
RUN apt update
RUN apt install portaudio19-dev -y
RUN pip install pyaudio
RUN pip install vosk

CMD ["python", "test.py"]
EXPOSE 8080