import pandas as pd
import requests
from bs4 import BeautifulSoup


prices = []
areas = []
rooms = []
floors = []

url = "https://tashkent.etagi.com/realty/?page=1"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

page_counter = 2
while len(prices) < 760:
    response = requests.get(url, headers = header)
    page = response.content
    soup = BeautifulSoup(page, 'html.parser')  
    cards = soup.find_all('div', class_= '_3AkUH templates-object-card')
  
    for card in cards:        
        card_area = card.find('div', class_ = 'templates-object-card__body')
        renovation_type = card_area.find('div', class_ = 'Y9CNb KBF2O _270PT')
        wrapper = card_area.find('div', class_ = 'templates-object-card__body__wrapper')
        price = wrapper.find('span', class_ = '_1s0Jo _2Ylcq').get_text()
        prices.append(price)
        
        div_of_spans = wrapper.find('div', class_ = 'templates-object-card__row templates-object-card__params')
        first_span = div_of_spans.find('span')
        room = first_span.find('a').text
        rooms.append(room)

        area = div_of_spans.select('div > span')[1].get_text(strip=True)
        areas.append(area)
        floor = div_of_spans.select('div > span')[2].get_text(strip=True)
        floors.append(floor)

    url = url[:-1]
    url += str(page_counter)
    # increment page number in the url
    page_counter += 1


counter = 0
for item in prices:
    print("Price #" + str(counter))
    counter += 1

df = pd.DataFrame.from_dict(
    {'Price': prices, 'Rooms': rooms, 'Area':areas, 'Floor': floors })
# save to excel file
df.to_excel('dataset.xlsx', header=True, index=False)    