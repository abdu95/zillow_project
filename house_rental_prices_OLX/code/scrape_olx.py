import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

urls = []
districts = []
prices = []
features = []

url = 'https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/?page=1'
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

page_counter = 2
while page_counter < 25:
    counter = 0
    response = requests.get(url, headers = header)
    page = response.content
    soup = BeautifulSoup(page, 'html.parser') 
    table = soup.find('table', class_ = 'fixed offers breakword redesigned')
    trs = table.find_all('tr', class_ = 'wrap')
    for tr in trs:
        url_of_house = tr.find('a', class_ = 'marginright5 link linkWithHash detailsLink')['href']
        urls.append(url_of_house)
        bottom = tr.find('td', class_ = 'bottom-cell')
        para_district = bottom.find('p', class_ = 'lheight16')
        district = para_district.find('span').get_text()
        districts.append(district)
        price_td = tr.find('td', class_ = 'wwnormal tright td-price')
        price = price_td.find('p', class_ = 'price').get_text()
        prices.append(price)
        
        house_response = requests.get(url_of_house, headers = header)
        house_page = house_response.content
        house_soup = BeautifulSoup(house_page, 'html.parser') 
        feature = house_soup.find('ul', class_ = 'css-sfcl1s')
        if feature != None:
            features.append(feature.get_text())
        else:
            features.append(' ')
        print(price + " " + str(counter))
        counter += 1
    time.sleep(1)

    url = url[:-1]
    url += str(page_counter)
    # increment page number in the url
    page_counter += 1


df = pd.DataFrame.from_dict(
    {'House_URL': urls, 'Price': prices, 'District': districts, 'Features': features})
# save to excel file
df.to_excel('dataset_olx_raw.xlsx', header=True, index=False) 