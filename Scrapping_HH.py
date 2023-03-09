import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
from tqdm import tqdm

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
head = Headers(browser='firefox', os='win').generate()

resp = requests.get(url, headers=head)
soup = BeautifulSoup(resp.text, 'html.parser')

cards_all = soup.find_all(class_='vacancy-serp-item__layout')

data = []
for card in tqdm(cards_all):

    # Название вакансии
    name = card.find('a', class_='serp-item__title').text
    # print(name)

    # Город
    city = card.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text

    # Ссылка на вакансию
    link = card.find('a')['href']
    # print(link)

    # Переходим по ссылке
    resp_2 = requests.get(link, headers=head)
    soup_2 = BeautifulSoup(resp_2.text, 'html.parser')

    vacancy_description = soup_2.find('div', class_='vacancy-description').text.lower()

    # Ищем в вакансии "django" или "flask"
    if 'django' not in vacancy_description and 'flask' not in vacancy_description:
        continue

    else:
        print('\n')
        print(name)
        print(link)
        print(city)

        name_company = soup_2.find('span', {'data-qa': 'bloko-header-2'}).text
        print(name_company)
        if soup_2.find('span', {'data-qa': 'vacancy-salary-compensation-type-net'}) != None:
            salary = soup_2.find('span', {'data-qa': 'vacancy-salary-compensation-type-net'}).text
            print(salary)
        else:
            print('з/п не указана')
            salary = 'з/п не указана'

        data.append({'вакансия': name, 'ссылка': link, 'город': city, 'з/п': salary})

with open('result.json', 'w', encoding='utf-8') as temp:
    json.dump(data, temp, ensure_ascii=False)



















































