Installation
## Prerequisites

- Python 3.11
- pip (Python package installer)
- Virtualenv
- Docker

## Clone the Repository

git clone https://github.com/NazimHusain/social.git
cd social

## Create Virtual Env And Activate it
python3 -m venv venv
source venv/bin/activate

## Install project requirements 
pip install -r requirements.txt


## make migratiuons and migrate
python manage.py makemigrations
python manage.py migrate

## create superuser
python manage.py createsuperuser

## built docker
docker-compose build

## run Docker
docker-compose up
