import json

from bs4 import BeautifulSoup
import requests


base_url = "http://quotes.toscrape.com"


def get_urls():
    urls = []
    page = 1

    while True:
        url = base_url + f"/page/{page}/"   
        urls.append(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        tag_a = soup.select_one("li.next a")
        
        if tag_a:
            url = tag_a.get("href")
            page += 1
            continue
        break
    return urls


def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

    

def spider(urls):
    authors_names = []

    quotes = []
    authors = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        divs = soup.select("div.quote")

        for div in divs:
            raw_tags = div.select("a.tag")
            q_tags = [tag.text for tag in raw_tags]
            q_author = div.select_one("small.author").text
            q_quote = div.select_one("span.text").text

            q_result = {"tags": q_tags, "author": q_author, "quote": q_quote}
            quotes.append(q_result)

            author_href = div.select_one("a").get("href")
            response = requests.get(base_url+author_href)
            soup = BeautifulSoup(response.text, "lxml")

            a_fullname = soup.select_one("h3.author-title").text.replace("\n", "").strip()

            if a_fullname not in authors_names:
                authors_names.append(a_fullname)

                a_born_date = soup.select_one("span.author-born-date").text
                a_born_location = soup.select_one("span.author-born-location").text
                a_description = soup.select_one("div.author-description").text.replace("\n", "").strip()

                a_result = {"fullname": a_fullname, "born_date": a_born_date, "born_location": a_born_location, "description": a_description}
                authors.append(a_result)
        
    return quotes, authors


if __name__ == "__main__":
    urls = get_urls()
    quotes, authors = spider(urls)
    save_data(quotes, "quotes.json")
    save_data(authors, "authors.json")