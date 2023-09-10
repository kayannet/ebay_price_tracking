import requests
# from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

# spaces represented with + sign
search_term = input('Search Term:')
search_term = search_term.replace(' ', '+')
max_page = 6

def get_data(search_term, page):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={search_term}&_sacat=0&LH_TitleDesc=0&LH_PrefLoc=1&LH_Complete=1&LH_Sold=1&imm=1&rt=nc&_pgn={page}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:

        product = {
            'title': item.find('div', {'class':'s-item__title'}).text,
            'soldprice': item.find('span', {'class': 's-item__price'}).text.replace('$', '').replace(',', '').strip(),
            'link': item.find('a', {'class': 's-item__link'})['href']
        }
        
        sold_date = item.find('div', {'class': 's-item__title--tag'})
        bids = item.find('span', {'class': 's-item__bids'})
        if sold_date:
            product['solddate'] = sold_date.find('span', {'class', 'POSITIVE'}).text
        else:
            product['solddate'] = 'NA'
        if bids:
            product['bids'] = bids.text
        else:
            product['bids'] = 'NA'

        productslist.append(product)
    return productslist

# search multiple pages
def parse_pages(max_pages):
    large_products_list = []
    page = 1
    while page != max_pages:
        soup = get_data(search_term, page)
        prodictslist = parse(soup)
        large_products_list.extend(prodictslist)
        print(f'Page {page} parsed.')
        page += 1
    
    return large_products_list

def output(productslist, search_term):
    products_df = pd.DataFrame(productslist)
    products_df.to_csv(search_term + '_output.csv', index = False)
    print('Saved to CSV')
    return

productslist = parse_pages(max_page)
output(productslist, search_term)

