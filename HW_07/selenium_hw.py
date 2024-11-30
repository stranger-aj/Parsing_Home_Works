# Выберите веб-сайт, который содержит информацию, представляющую интерес для извлечения данных. Это может быть новостной сайт, 
# платформа для электронной коммерции или любой другой сайт, который позволяет осуществлять скрейпинг (убедитесь в соблюдении условий обслуживания сайта).
# Используя Selenium, напишите сценарий для автоматизации процесса перехода на нужную страницу сайта.
# Определите элементы HTML, содержащие информацию, которую вы хотите извлечь (например, заголовки статей, названия продуктов, цены и т.д.).
# Используйте BeautifulSoup для парсинга содержимого HTML и извлечения нужной информации из идентифицированных элементов.
# Обработайте любые ошибки или исключения, которые могут возникнуть в процессе скрейпинга.
# Протестируйте свой скрипт на различных сценариях, чтобы убедиться, что он точно извлекает нужные данные.
# Предоставьте ваш Python-скрипт вместе с кратким отчетом (не более 1 страницы), который включает следующее: URL сайта. 
# Укажите URL сайта, который вы выбрали для анализа. Описание. Предоставьте краткое описание информации, которую вы хотели извлечь из сайта. 
# Подход. Объясните подход, который вы использовали для навигации по сайту, определения соответствующих элементов и извлечения нужных данных. 
# Трудности. Опишите все проблемы и препятствия, с которыми вы столкнулись в ходе реализации проекта, и как вы их преодолели. Результаты. 
# Включите образец извлеченных данных в выбранном вами структурированном формате (например, CSV или JSON). 
# Примечание: Обязательно соблюдайте условия обслуживания сайта и избегайте чрезмерного скрейпинга, который может нарушить нормальную работу сайта

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import csv

url_base = "https://www.labirint.ru/"
to_find = "мастера буддизма"
options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options = options)
driver.get(url_base)

time.sleep(5)
# ищем поле для поиска по ID
input = driver.find_element(By.ID, 'search-field')
input.send_keys(to_find)
input.send_keys(Keys.ENTER)
actions = ActionChains(driver)

books = []
page = 1

while True:
    time.sleep(2)
    items = driver.find_elements(By.XPATH,"//div[@data-product-id]")
    print('Page: ', page)
    print('Count of items: ', len(items))
    # print(*items, sep='\n')
    page += 1
    # сбор данных по каждому найденному элементу (книге)
    for item in items:
        try:
            name = item.find_element(By.XPATH, "./a[@class = 'product-card__name']").text
        except:
            name = None
        try:
            url = item.find_element(By.XPATH, "./a[@class = 'product-card__name']").get_attribute("href")
        except:
            url = None
        try:
            cost_text = item.find_element(By.XPATH, ".//div[@class = 'product-card__price-current']").text
            cost = float('.'.join(re.findall(r'\d+', cost_text)))
        except:
            cost = None
        try:
            author = item.find_element(By.XPATH, ".//div[@class = 'product-card__author']/a[@title]").get_attribute("title")
        except :
            author = None
        book_dict = {
            'name': name,
            'author': author,
            'url': url,
            'cost': cost
        }
        books.append(book_dict)
    # print(*books, sep='\n')

    try:
        # Переключение страниц
        btn_next = driver.find_element(By.XPATH, "//a[@title='Следующая']")
        actions.move_to_element(btn_next)
        actions.perform()
        time.sleep(1)
        btn_next.click()
    except  Exception:
        break

# сохранение в файл csv
keys = books[0].keys()
with open('books.csv', 'w', newline='', encoding="UTF-8") as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames = keys)
    dict_writer.writeheader()
    for line in books:
        dict_writer.writerow(line)