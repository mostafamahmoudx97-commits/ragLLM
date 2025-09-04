## Requierments
--python 3.8 or later  

## Add your environment variable 
 cp  .env.example .env

 ## Run the FastAPi server
 uvicorn main:app --reload host 0.0.0.0

 ## Optional) Setup you command line interface for better readability
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "