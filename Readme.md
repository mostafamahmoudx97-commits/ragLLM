##  Requirements

--python 3.8 or later  

## Add your environment variable

 cp  .env.example .env

## to install your dependancies

pip install -r requirements.txt

## Run the FastAPi server

uvicorn main:app --reload  --host 0.0.0.0

## (Optional) Setup you command line interface for better readability

export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "

## for macOS

export PROMPT='%F{green}%n@%m:%~%f
%# '

## Run Dockeer compose service up

copy .env.example to .env and add you values

## cohere generation model

command-a-03-2025

## alembic create revision version

alembic revision --autogenerate -m "initial commit"

## alembic deploy version

alembic upgrade head
