#Introduction
This a small scale web scraping project!

#Getting Started
1. Install the dependencies from the requirements.txt file.
2. Start the RabbitMQ server on the host machine using the following command:
    $ sudo rabbitmqctl start
3. Start the Celery Worker from the project root directory using the following command:
    $ celery -A scraper worker -l info
4. Start the Django Application by running the following command in the project root directory:
    $ python mange.py runserver

#API End-points:
1. Pass a list of URLs(str) with 'urls' as the key in the body as a post request on the following to kick off the crawler task:
    http://127.0.0.1:8000/crawl?
   A task ID would be returned.
2. Pass the task ID to the following endpoint as a get request to get the status of the task:
    ex- http://127.0.0.1:8000/status?id=60eea48c-0e30-4f76-b8ab-520f6314c038
3. Query the DB using the following to get all the rows:
    http://127.0.0.1:8000/data
   You can get individual row data by using a particular ID:
    ex- http://127.0.0.1:8000/data/1
4. Pass the price as 'price' as the key in the body as a post request on the following to get the 10 products which have prices close to the given price:
    http://127.0.0.1:8000/closest_price
