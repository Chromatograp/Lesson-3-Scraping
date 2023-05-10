import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from list_to_text import text # Для извлечения текста из списков была написана отдельная функция

# Парсинг данных. HTML, Beautiful Soup. Урок 3.
# Спарсить цитаты с сайта Quotes to Scrape. Необходимо извлечь саму цитату, автора и список тегов.
# Задание со звёздочкой: спарсить все цитаты на сайте, а не только с первой страницы. При парсинге
# желательно использовать разные методы для получения необходимой информации.

page = 0 # Старт отсчета страниц
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'} # Заголовки для передачи сайту

dic = {'quotes': [], 'authors': [], 'tags': []} # Словарь для записи информации
while True:
       """
       В данной функции проходим циклом по всем страницам сайта и останавливаемся, когда на странице перестает появляться контент.
       """
       url = f'https://quotes.toscrape.com/page/{page}/' # Страница, номер которой будет меняться с каждой итерацией цикла
       response = requests.get(url, headers=headers) # Запрос страницы
       soup = bs(response.content, 'html.parser') # Передача страницы парсеру
       page += 1
       if soup.find('span', {'class': 'text'}) == None: # Проверка страницы на наличие контента
              break # При отсутствии контента цикл прерывается
       else:
              try:
                     info = soup.find_all('div', {'class': 'quote'}) # В противном случае ищем указанный тег
                     for i in range(len(info)): # И собираем информацию со всех интересующих нас тегов
                            var = info[i]
                            dic['quotes'].append(var.find('span', {'class': 'text'}).text)
                            dic['authors'].append(var.find('small', {'class': 'author'}).text)
                            dic['tags'].append(text(var.find_all('a', {'class': 'tag'}))) # Способ сбора информации с данного
                            # тега отличается, так как на один родительский тег приходиться несколько одноуровневых тегов этого класса
              except AttributeError: # Чтобы списки были равными по длине, при отсутствии информации прибавляем элемент None
                     dic['quotes'].append(None)
                     dic['authors'].append(None)
                     dic['tags'].append(None)

# Записываем полученный словарь в датафрейм и файл csv
df = pd.DataFrame(dic)
df.to_csv('quotes_to_scrape.csv')
