pip install virtualenv
python:3.10.12 -m venv ouijaEnv
source ouijaEnv/bin/activate

// requerimientos
pip list  
pip freeze > requirements.txt

pip install -r requirements.txt
