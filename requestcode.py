from itertools import cycle
from random import choice
import requests
from bs4 import BeautifulSoup
import proxyScrape
import tenacity
import re
from lxml import html
import datetime

proxyPool = proxyScrape.getProxy()
proxyPool = cycle(proxyPool)
header = [
    "Mozilla/5.0 (Windows NT 10.0; Win64;x64; rv:66.0) Gecko/20100101 Firefox/66.0", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
]
header = cycle(header)

title_xpath = '//*[@id="productTitle"]'
price_xpath1 = '[//*[@id="priceblock_ourprice" or @id="priceblock_dealprice" or @id="priceblock_saleprice"]'
price_xpath2 = '//*[@id="priceblock_ourprice"]'
rating_xpath = '//*[@id="acrPopover"]/span[1]/a/i[1]/span'

def get_date():
    return datetime.date.today().strftime('%Y-%m-%d')

def asin_from_url(url):
    regex = "/([a-zA-Z0-9]{10})(?:[/?]|$)"
    asin = re.findall(regex, url)[0]
    return asin

def url_from_asin(asin):
    url = f'https://www.amazon.in/dp/{asin}'
    return url


@tenacity.retry(stop=tenacity.stop_after_attempt(10), wait=tenacity.wait_fixed(0.5))
def get_response(url):					
    global header
    global proxyPool
    headers = {"User-Agent": next(header), "Accept-Encoding":"gzip, deflate","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","DNT":"1","Connection":"close","Upgrade-Insecure-Requests":"1"}
    proxy = next(proxyPool)
    asin = asin_from_url(url)
    url = url_from_asin(asin)
    r = requests.get(url,headers=headers,proxies={'http':proxy})
    if r.status_code !=200:
        raise Exception
    return r.content

#@tenacity.retry(stop=tenacity.stop_after_attempt(10), wait=tenacity.wait_fixed(0.5))
def get_info(url):
    html_doc = get_response(url)
    parsed_page = html.fromstring(html_doc)
    title = parsed_page.xpath('//*[@id="productTitle"]/text()')[0].replace(",", "").strip()
    # if len(title) > 0:
    #     title = title[0].replace(",", "").strip()
    # else:
    #     title = "Title not mentioned"

    price = parsed_page.xpath('//*[@id="priceblock_ourprice" or @id="priceblock_dealprice" or @id="priceblock_saleprice"]/text()')[0].replace("\xa0", "")
    price = float(price.strip().replace('₹','').replace(',',''))
    # if len(price) > 0:
    #     price = price[0].replace("\xa0", "")
    # else:
    #     price = "Price not mentioned"

    rating = parsed_page.xpath('//*[@id="acrPopover"]/span[1]/a/i[1]/span/text()')[0].strip().split()[0]
    # if len(rating) > 0:
    #     rating = rating[0]
    # else:
    #     rating = "Rating not mentioned"

    # soup = BeautifulSoup(html_doc,'html.parser')
    # dom = etree.HTML(str(soup))
    # title = dom.xpath(title_xpath)[0].text
    # price = dom.xpath(price_xpath1)[0].text
    # price = dom.xpath(price_xpath2)[0].text
    # rating = dom.xpath(rating_xpath)[0].text
    # print(title,rating,price)

    # title = ' '.join(x.lower() for x in title.split())
    # rating = rating.strip().split()[0]
    # price = float(price.strip().replace('₹','').replace(',',''))

    search_date = datetime.date.today().strftime('%Y-%m-%d')
    url = url
    asin = asin_from_url(url)
    product_id = asin + datetime.datetime.now().strftime("%m/%d/%Y%H:%M:%S")
    info = {
        product_id : product_id,
        asin : asin,
        title : title,
        url : url,
        search_date : search_date,
        price : price,
        rating : rating
    }

    return info

    


