pip install virtualenv
python:3.10.12 -m venv ouijaEnv
source env/bin/activate

// requerimientos
pip list  
pip freeze > requirements.txt

pip install -r requirements.txt

yes culo