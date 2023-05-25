from bs4 import BeautifulSoup
import csv
import requests


def get_items(url):
    """
    Get news items from a given url.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'xml')
    items = soup.find_all('item')
    return items


def get_categories(item):
    """
    Get categories from a news item.
    """
    category_items = item.find_all('category')
    return [i.text for i in category_items]


def get_info(item):
    """
    Get information for a single item.
    """
    title = item.find('title').text
    link = item.find('link').text
    enclosure = item.find('enclosure').get('url')
    description = item.find('description').text
    category = get_categories(item)
    pubDate = item.find('pubDate').text
    result = {'title': title, 'link': link, 'enclosure': enclosure,
              'description': description, 'category': category, 'pubDate': pubDate}
    return result


def save_csv(data, filename):
    """
    Save data to a csv file.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        field_names = ['title', 'link', 'enclosure',
                       'description', 'category', 'pubDate']
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    url = 'https://sport.ua/uk/rss/all'
    items = get_items(url)

    news = []
    for item in items:
        new = get_info(item)
        news.append(new)

    filename = 'news_sport_ua.csv'
    save_csv(news, filename)
