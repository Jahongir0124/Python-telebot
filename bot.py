import json
import requests
from bs4 import BeautifulSoup
from http import HTTPStatus
import threading
journals_ru = []
journals_uz = []
journals_en = []
d={}
i = 1
def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func
def save_data(data_ru,data_uz,data_en):
    di = {}
    di['ru'] = data_ru
    di['uz'] = data_uz
    di['en'] = data_en
    with open('save.json', 'w', encoding='utf-8') as f:
         (json.dump(di, f, ensure_ascii=False, indent=4))
while True:
    website_ru = requests.get(f"https://www.oriens.uz/ru/archive/{i}/")
    html_ru = BeautifulSoup(website_ru.content, "html.parser")
    for journal in html_ru.select(".last_posts__big"):
            image = journal.select('img[src]')
            element = {
                'name': journal.select(".last_posts__title")[0].text.strip(),
                'description': journal.select(".last_posts__description")[0].text.strip(),
                'pub_date': journal.select(".news-meta span")[0].text.strip(),
                'link': f"https://www.oriens.uz{journal.select('a')[0]['href']}",
                'link_img':f"https://www.oriens.uz{journal.select('img')[0]['src']}"
            }
            journals_ru.append(element)
    website_uz = requests.get(f"https://www.oriens.uz/archive/{i}/")
    html_uz = BeautifulSoup(website_uz.content, "html.parser")
    for journal in html_uz.select(".last_posts__big"):
        image = journal.select('img[src]')
        element = {
            'name': journal.select(".last_posts__title")[0].text.strip(),
            'description': journal.select(".last_posts__description")[0].text.strip(),
            'pub_date': journal.select(".news-meta span")[0].text.strip(),
            'link': f"https://www.oriens.uz{journal.select('a')[0]['href']}",
            'link_img': f"https://www.oriens.uz{journal.select('img')[0]['src']}"
        }
        journals_uz.append(element)
    website_en = requests.get(f"https://www.oriens.uz/en/archive/{i}/")
    html_en = BeautifulSoup(website_en.content, "html.parser")
    for journal in html_en.select(".last_posts__big"):
        image = journal.select('img[src]')
        element = {
            'name': journal.select(".last_posts__title")[0].text.strip(),
            'description': journal.select(".last_posts__description")[0].text.strip(),
            'pub_date': journal.select(".news-meta span")[0].text.strip(),
            'link': f"https://www.oriens.uz{journal.select('a')[0]['href']}",
            'link_img': f"https://www.oriens.uz{journal.select('img')[0]['src']}"
        }
        journals_en.append(element)
    if i ==4:
        break
    i+=1
setInterval(save_data(journals_ru,journals_uz,journals_en),10)