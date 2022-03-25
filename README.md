
# Project Build Instructions

#### Make virtual environment
python3 -m venv env 
#### Activate virtual environment
source env/bin/activate 
#### Install requirements 
pip install -r requirements.txt

#### Run the server on port 8000
python3 manage.py runserver

## API
POST 
http://localhost:8000/route

body = {
    "src_lat":"37.802289", 
    "src_lng":"-122.413034",
    "dst_lat":"37.787375",
    "dst_lng":"-122.446110"
}



