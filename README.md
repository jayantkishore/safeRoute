
# Project Build Instructions

#### Make virtual environment
python3 -m venv env 
#### Activate virtual environment
source env/bin/activate 
#### Install requirements 
pip install -r requirements.txt
#### Paste API Keys
Search for variables BING_API_KEY and HERE_API_KEY and replace their value with your own API Keys obtained from [Bing Maps](https://docs.microsoft.com/en-us/bingmaps/getting-started/bing-maps-dev-center-help/getting-a-bing-maps-key) and [Here Maps](https://developer.here.com/tutorials/getting-here-credentials/).
#### Run the server on port 8000
python3 manage.py runserver


