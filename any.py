from bs4 import BeautifulSoup
import requests


base_url = "http://quotes.toscrape.com"



response = requests.get(base_url)
soup = BeautifulSoup(response.text, "lxml")
divs = soup.select("div.quote")
for div in divs:
    raw_tags = div.select("a.tag")
    tags = [tag.text for tag in raw_tags]
    author = div.select_one("small.author").text
    qoute = div.select_one("span.text").text
    result = {"tags": tags, "author": author, "quote": qoute}
    print(result)
    