
import sys
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
def web_scraping_first(url):
    """
    It takes url as parameters, use beautifulsoup and requests for web scraping
    and return list of list of data
    """
    response = requests.get(url)
    response.raise_for_status()
    data = response.text
    soup = BeautifulSoup(data, "xml")
    items = soup.find_all("item")
    date = soup.find("lastBuildDate").text
    dt = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
    date = dt.strftime("%Y%m%d")

    li_of_li = []
    for item in items:
        new_list = []
        cells = item.find_all(["title", "pubDate", "description"])
        res = [cell.get_text(strip=True) for cell in cells]
        new_soup = BeautifulSoup(res[2], "html.parser")
        title = res[0]
        published_date = res[1]
        description = new_soup.text
        links = new_soup.find_all(["a"])
        source_link = links[0]["href"]
        source_name = links[1].text
        new_list.extend([title, published_date, description, source_name, source_link])
        li_of_li.append(new_list)

        key = (date, source_name)
    return li_of_li, key


def web_scraping_second(url):
    response = requests.get(url)
    response.raise_for_status()
    data = response.text
    soup = BeautifulSoup(data, "xml")
    items = soup.find_all("item")
    date = soup.find("lastBuildDate").text
    dt = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
    date = dt.strftime("%Y%m%d")
    li_of_li = []
    for item in items:
        new_list = []
        cells = item.find_all(["title", "pubDate", "description", "link"])
        # res = [cell.get_text(strip=True) for cell in cells]
        title_tag = item.find("title")
        pub_tag = item.find("pubDate")
        desc_tag = item.find("description")
        link_tag = item.find("link")

        title = title_tag.get_text(strip=True) if title_tag else ""
        published_date = pub_tag.get_text(strip=True) if pub_tag else ""
        description = desc_tag.get_text(strip=True) if desc_tag else ""
        source_link = link_tag.get_text(strip=True) if link_tag else ""

        source_name = soup.title.text
        new_list.extend([title, published_date, description, source_name, source_link])
        li_of_li.append(new_list)
        key = (date, source_name)
    return li_of_li, key


urls = [
    "https://english.onlinekhabar.com/feed",
    "https://english.nepalnews.com/feed",
    "https://english.ratopati.com/feed",
    "https://www.kathmandutribune.com/feed/",
]


# web_scraping_second("https://www.kathmandutribune.com/feed/")
def to_csv(url):
    if "onlinekhabar" in url:
        data, val = web_scraping_first(url)
        name = val[0] + val[1].split()[0]
        with open(f"{name}.csv", "w", encoding="utf-8") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(
                ["title", "published_date", "description", "source_name", "source_link"]
            )
            writer.writerows(data)
    else:
        data, val = web_scraping_second(url)
        name = val[0] + val[1].split()[0]
        with open(f"{name}.csv", "w", encoding="utf-8") as file_obj:
            writer = csv.writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                ["title", "published_date", "description", "source_name", "source_link"]
            )
            writer.writerows(data)


for url in urls:
    to_csv(url)
