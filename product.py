import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

def search_url(search_term, page_number):
    template = 'https://www.myntra.com/{}?rawQuery={}&p={}'
    return template.format(search_term, search_term, page_number)

driver = webdriver.Chrome()

org_url = input('enter your search term: ')

brands = []
price=[]
original_price=[]
description=[]
ratings=[]
product_url=[]

for i in range(1, 2):
    driver.get(search_url(org_url, i))
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    try:
        brand = soup.find_all('h3', class_="product-brand")
        for a in brand:
            brands.append(a.text)
    except AttributeError:
        continue
        
    #price
    try:
        pr = soup.find_all('span',class_="product-discountedPrice")
        for b in pr:
            price.append(int(b.text.strip('Rs. ')))
    except AttributeError:
        price.append(None)
        
    missing_count = len(brands) - len(price)
    if missing_count > 0:
        price.extend([None]*missing_count)
    
    #original price
    try:
        mrp = soup.find_all('span', class_ = 'product-strike')
        for c in mrp:
            original_price.append(int(c.text.strip('Rs. ')))
    except AttributeError:
        original_price.append(None)
        
    missing_counts = len(brands) - len(original_price)
    if missing_counts > 0:
        original_price.extend([None]*missing_counts)
    
    #description
    try:
        des = soup.find_all('h4', class_='product-product')
        description.extend([i.text for i in des])
    except AttributeError:
        description =' '
        
    #product url

    try:
        li_elements = soup.find_all('li', class_="product-base")
        for d in li_elements:
            a_elements = d.find_all('a', {'data-refreshpage': 'true', 'target': '_blank'})
            for a in a_elements:
                href = 'http://myntra.com/' + a['href']
                product_url.append(href)
    except AttributeError:
        product_url=' '

        
driver.close()

df = pd.DataFrame(columns=['brand_name','price','original_price','description','product_url'])
df['brand_name'] = brands
df['price']=price
df['original_price']=original_price
df['description']=description
df['product_url']=product_url

df.to_csv("myntra_" + org_url + ".csv")
