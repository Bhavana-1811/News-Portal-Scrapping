import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


def get_data(response_text, df1):
    soup = BeautifulSoup(response_text, features = "html.parser")
    tags = soup.find_all(attrs={"itemprop": "headline"})
    article_content = soup.find_all(attrs={"itemprop": "articleBody"})
    date_posted = soup.find_all(attrs={"class": "date"})
    author = soup.find_all(attrs={"class": "author"})
    for i in range(len(tags)):
        df1 = df1.append({'Tags':tags[i].text, 'Article Content': article_content[i].text, 'Date posted': date_posted[i].text, 'Author': author[i].text}, ignore_index= True)
    return df1

def get_headers():
    return {
        "accept": "/",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-IN,en-US;q=0.9,en;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "_ga=GA1.2.474379061.1548476083; _gid=GA1.2.251903072.1548476083; __gads=ID=17fd29a6d34048fc:T=1548476085:S=ALNI_MaRiLYBFlMfKNMAtiW0J3b_o0XGxw",
        "origin": "https://inshorts.com",
        "referer": "https://inshorts.com/en/read/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }


df = pd.DataFrame(columns=['Tags', 'Article Content', 'Date posted', 'Author'])
url = 'https://inshorts.com/en/read'
response = requests.get(url)
data = get_data(response.text, df)

# get more news
url = 'https://inshorts.com/en/ajax/more_news'
news_offset = "apwuhnrm-1"

while True:
    response = requests.post(url, data={"category": "", "news_offset": news_offset}, headers=get_headers())
    if response.status_code != 200:
        print(response.status_code)
        break

    response_json = json.loads(response.text)
    data = get_data(response_json["html"], data)
    news_offset = response_json["min_news_id"]

print(data['Tags'].count())
data.to_csv('news_portal_all.csv', index=False, encoding='utf-8')
