// linux
pip install virtualenv
python3 -m venv ouijaEnv
source ouijaEnv/bin/activate
// windows
source ouijaEnv/Scripts/activate
// 
// requerimientos
pip list  
pip freeze > requirements.txt

pip install -r requirements.txt

// nltk
python -m nltk.downloader all



// para arreglar ciertos errores de pyaudio 
sudo apt install portaudio19-dev