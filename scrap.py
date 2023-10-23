import requests
from bs4 import BeautifulSoup
from persiantools.digits import fa_to_en
from datetime import datetime
import pandas as pd
def date_time_convertor(date_time):
    dt = fa_to_en(date_time)
    d = datetime.strptime(dt, "(%H:%M) %Y/%m/%d").date()
    t = datetime.strptime(dt, "(%H:%M) %Y/%m/%d").time()

    return d, t


url = "https://akharinkhabar.ir/sport"

response = requests.get(url)
response.encoding = "utf-8"

page = BeautifulSoup(response.text, "html.parser")
li_list = page.find_all("li")

news_list = []

for li in li_list:
    try:
        if li["class"] == ["live-feed-news-item", "list", "has-image"]:
            d, t = date_time_convertor(li.p.span.text)
            news = {
                "title": li.h5.text,
                "image": li.img["src"],
                "link": "https://akharinkhabar.ir/" + li.a["href"],
                "date": d,
                "time": t
            }
            news_list.append(news)


    except:
        pass


df = pd.DataFrame(news_list)
df.to_csv("news.csv")