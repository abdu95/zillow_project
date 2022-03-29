import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


prices = []
room_area_floors = []
districts = []
house_ids = []
renovation_types = []
built_years = []
span_walls = []

url = "https://tashkent.etagi.com/realty/?page=1"
url_house_main = 'https://tashkent.etagi.com'
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

page_counter = 2
while len(districts) < 760:
    counter = 0

    response = requests.get(url, headers = header)
    page = response.content
    soup = BeautifulSoup(page, 'html.parser')  
    cards = soup.find_all('div', class_= '_3AkUH templates-object-card')
  
    for card in cards: 
        a_of_house = card.find('a', class_ = 'templates-object-card__slider') 
        url_of_house = url_house_main + a_of_house['href']
        house_response = requests.get(url_of_house, headers = header)
        house_page = house_response.content
        house_soup = BeautifulSoup(house_page, 'html.parser')  
        room_area_floor = house_soup.find('span', class_ = '_3_KKe').get_text()
        room_area_floors.append(room_area_floor)

        div_of_price = house_soup.find('div', class_ = '_3wbiI')
        span_price = div_of_price.find('span', class_ = '_1s0Jo')
        prices.append(span_price.text)

        district = house_soup.find('div', class_ = 'desk-object-address__main _3DJU-')
        districts.append(district.text)
        
        house_id = house_soup.find('span', class_ = '_7hb5_').get_text()
        house_ids.append(house_id)

        ul_of_lis = house_soup.find('ul', class_ = '_2QWeq')
        third_li = ul_of_lis.select('ul > li')[2]
        span_renovation = third_li.select('li > span')[1]
        renovation_types.append(span_renovation.text)
        
        fourth_li = ul_of_lis.select('ul > li')[3]
        span_built_year = fourth_li.select('li > span')[1]
        built_years.append(span_built_year.text)
        
        print(house_id + " " + str(counter))
        counter += 1
    time.sleep(1)

    url = url[:-1]
    url += str(page_counter)
    # increment page number in the url
    page_counter += 1



df = pd.DataFrame.from_dict(
    {'House_id': house_ids, 'Price': prices, 'District': districts, 'Room_area_floor': room_area_floors, 'Renovation_types': renovation_types, 'Built_years': built_years})
# save to excel file
df.to_excel('dataset.xlsx', header=True, index=False)    
*