# AvaTrade
## Running the API Test
Install the prerequsites:
> pip install -r requirements.txt

Create the DB:
> python manage.py migrate

Run the server:
> python manage.py runserver

Run the bot:
> cd avatrade\bot

> python bot.py

## Configuration
* For configuring the bot, please update the avatrade\bot\bot_config.yaml
* For configuring the socail network app of our API, please update the avatrade\social_network\apps.py