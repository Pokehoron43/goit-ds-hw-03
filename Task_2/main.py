import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError

BASE_URL = "http://quotes.toscrape.com"

def connect_db():
    try:
        client = MongoClient(
            "mongodb+srv://Moroz_Yevhen_db_user:pokenyxandEX36@task1.4zatt2b.mongodb.net/?appName=Task1",
            server_api=ServerApi("1")
        )

        db = client["Task_2"]
        return db["quotes"], db["authors"]

    except PyMongoError as e:
        print(f"Connection error: {e}")
        return None, None


def insert_quotes(collection, data):
    try:
        collection.insert_many(data)
        print("Quotes added.")
    except PyMongoError as e:
        print(f"Insert error: {e}")


def insert_authors(collection, data):
    try:
        collection.insert_many(data)
        print("Authors added.")
    except PyMongoError as e:
        print(f"Insert error: {e}")


def scrape_quotes():
    quotes_list = []
    authors_dict = {}

    url = "/"

    while url:
        response = requests.get(urljoin(BASE_URL, url))
        soup = BeautifulSoup(response.text, "html.parser")

        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]

            quotes_list.append({
                "tags": tags,
                "author": author,
                "quote": text
            })

            if author not in authors_dict:
                author_link = quote.find("a")["href"]
                author_url = urljoin(BASE_URL, author_link)

                author_page = requests.get(author_url)
                author_soup = BeautifulSoup(author_page.text, "html.parser")

                authors_dict[author] = {
                    "fullname": author_soup.find("h3", class_="author-title").text.strip(),
                    "born_date": author_soup.find("span", class_="author-born-date").text.strip(),
                    "born_location": author_soup.find("span", class_="author-born-location").text.strip(),
                    "description": author_soup.find("div", class_="author-description").text.strip()
                }

        next_button = soup.find("li", class_="next")
        url = next_button.find("a")["href"] if next_button else None

    return quotes_list, list(authors_dict.values())



def save_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



def main():
    quotes_list, authors_list = scrape_quotes()

    
    save_to_json("quotes.json", quotes_list)
    save_to_json("authors.json", authors_list)

    
    quotes_collection, authors_collection = connect_db()

    if quotes_collection and authors_collection:
        insert_quotes(quotes_collection, quotes_list)
        insert_authors(authors_collection, authors_list)


if __name__ == "__main__":
    main()