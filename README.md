# amazon_scraper
# Flask Api with periodic scraper using celery beat
Flask api to obtain Amazon product details(title, price, rating). Celery to do asynchronous scraping with the help of celery beat to perform the task periodically.

# Procedure
1) Created a celery app to integrate with existing flask app.
2) Created a task function to perform the scraping.
3) Added celery beat to periodically call the task function.
4) If there is a price change db will be updated.

# Working
* Celery will add the task to the message broker(rabbitmq).
* This task will be assigned to the worker.
* Celery beat will schedule the task periodically.
* The perioidic_scraper function will check for price change.
* If there is a price change then a new row will be added to the db for the same product with updated price.

# Requirements
* Python 3.7.6
* Flask 1.1.2
* Werkzeug 1.0.1
* lxml 4.6.3
* requests 2.25.1
* Flask-SQLAlchemy 2.5.1
* Celery 5.0.5
* Redis

# Install dependencies of entire tasks at once
Use `pip3 install -r requirements.txt`

# Commands to run 
Flask app - type `python amazon_api.py` in the terminal.
Celery worker - type `celery -A tasks.celery_app worker --pool=solo` in the terminal.
Celery beat - type `celery -A tasks.celery_app beat` in the terminal.
