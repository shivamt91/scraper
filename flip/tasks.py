import celery
from celery.utils.log import get_task_logger
from bs4 import BeautifulSoup
import requests
import re
from . models import Data

logger = get_task_logger(__name__)


@celery.task(bind=True)
def start_crawl(self, urls):
    if isinstance(urls, list):
        total_urls = len(urls)
        url_no = 1

        for url in urls:
            self.update_state(state="IN PROGRESS", meta={
                "total_urls": total_urls,
                "url_no getting crawled": url_no,
                "url getting crawled": url, }
            )
            get_product_details(url, 1)
            url_no += 1
    else:
        return 'Please provide a list()!'


def get_product_details(url, curr_page):
    curr_url = url + '&page=' + str(curr_page)
    response = requests.get(curr_url)
    plain_text = response.text
    soup = BeautifulSoup(plain_text, 'lxml')

    domain = 'https://www.flipkart.com'

    for product in soup.select('._1HmYoV._35HD7C > .bhgxx2.col-12-12 > ._3O0U0u'):
        item = dict({
            "name": product.select_one('div > div > a > ._1-2Iqu.row > div > ._3wU53n').string,
            "url": domain + product.select_one('div > div > a').get('href'),
            "price": int(product.select_one('div > div > a > ._1-2Iqu.row > .col.col-5-12._2o7WAb > div > div > ._1vC4OE._2rQ-NK').string.replace('₹', '').replace(',', '')),
        })

        ingest_data(item)

    str_to_parse = soup.select_one('._2zg3yZ > span').string
    next_page = curr_page + 1
    total_pages = int(re.match('Page [\d]+ of ([\d]+)', str_to_parse).group(1))

    if next_page <= total_pages:
        get_product_details(url, next_page)


def ingest_data(item):
    data = Data(name=item['name'], url=item['url'], price=item['price'], )
    data.save()
