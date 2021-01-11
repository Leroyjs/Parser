import requests
import csv
from bs4 import BeautifulSoup


# &start=251&ref_=adv_nxt
URL_TEST = 'https://www.imdb.com/search/title/?title=God&release_date=1960-01-01,2010-12-31&user_rating=2.8,10.0&countries=us&count=50'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': '*/*'}
HOST = 'https://www.imdb.com'

CONFIGURATIONS = {
    'title': 'name',
    'release_date': '1960-01-01,2010-12-31',
    'user_rating': '2.8,10.0',
    'countries': 'us'
}
URL = 'https://www.imdb.com/search/title/?title='+CONFIGURATIONS['title']+'&release_date='+CONFIGURATIONS['release_date']+'&user_rating='+CONFIGURATIONS['user_rating']+'&countries='+CONFIGURATIONS['countries']+'&count=50'





def get_blocks(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    film_details = soup.select('div#titleDetails div.txt-block')
    details = [tag.get_text(strip=True) for tag in film_details]
    print('Получаем информацию с блоков по ссылке ' + url)

    d = ''
    for i in details:
        d += i.replace('\n', '\xa0').replace('IMDbPro\xa0»', '').replace(u'See more\xa0»', u'').replace(u'Show more on',
                                                                                                        u'').replace(
            u'See full technical specs\xa0»', u'').replace(u'Edit', u'').replace(u'Details', u'').replace('|', ',')
    return d


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)

    print('Получаем HTML')

    if response.status_code == 200:
        return response


def get_content(html, film_list_all):

    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', class_='lister-item-content')
    COUNT = 0

    for item in items:
        COUNT += 1
        print(COUNT)
        film_attributes = {
            'title': '',
            'genres': '',
            'rating': '',
            'stars': '',
            'block': ''
        }
        try:
            title = item.find('h3', class_='lister-item-header').find('a')
            link = HOST + title['href']
            film_attributes['block'] = get_blocks(link)
            film_attributes['title'] = title.get_text(strip=True)
        except Exception as e:
            print(e)
        try:
            genres = item.find('p', class_='text-muted').find('span', class_='genre')
            film_attributes['genres'] = genres.get_text(strip=True)
        except Exception as e:
            print(e)

        try:
            rating = item.find('strong')
            film_attributes['rating'] = rating.get_text(strip=True)
        except Exception as e:
            print(e)

        try:
            stars = item.find_all('p')[2].find_all('a')[1:]
            newStars = ''
            for star in stars:
                newStars += star.get_text(strip=True) + ', '
            newStars = newStars[:-2]
            film_attributes['stars'] = newStars
        except Exception as e:
            print(e)

        film_list_all.append(film_attributes)

    return COUNT


def write_to_csv(film_list):
    try:
        keys = film_list[0].keys()
        with open('Films.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            print(film_list)
            dict_writer.writerows(film_list)
    except Exception as ex:
        print(ex)
        return False


def parse():
    COUNT = 1
    film_list_all = []
    IS_END = False

    while (not IS_END) and COUNT <= 1000:
        print(IS_END and COUNT <= 1000)
        print(URL + '&start=' + str(COUNT) + '&ref_=adv_nxt')
        html = get_html(URL + '&start=' + str(COUNT) + '&ref_=adv_nxt')
        LOCAL_COUNT = get_content(html, film_list_all)
        COUNT += LOCAL_COUNT
        print('Всего объектов: ' + str(COUNT - 1))
        if LOCAL_COUNT < 50:
            IS_END = True
            print('Объекты кончились')

    write_to_csv(film_list_all)
    print('Done')


parse()
