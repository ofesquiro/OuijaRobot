AUDIO_DEVICE_ID=$(python src/DeviceInputInfoGatherer.py)
export AUDIO_DEVICE_ID
echo $AUDIO_DEVICE_ID
#python src/main.py
docker-compose up
timeout /t 15