sudo apt install python3.10-venv
python3 -m venv ouijaEnv
source ouijaEnv/bin/activate
curl https://pyenv.run | bash

sudo apt upgrade
sudo apt update
pip install requests
pip install speechRecognition
sudo apt install portaudio19-dev -y
sudo apt-get install python3-pyaudio
pip install pyaudio
pip3 install pygame
pip3 install requests

sudo ubuntu-drivers install

sudo apt-get remove --purge alsa-base
sudo apt-get remove --purge pulseaudio

sudo apt-get install alsa-base
sudo apt-get install pulseaudio

sudo alsa force-reload

