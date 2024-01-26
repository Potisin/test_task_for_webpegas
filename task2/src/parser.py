import aiohttp
from bs4 import BeautifulSoup
import csv
import asyncio
from urllib.parse import urljoin


# Функция для получения HTML контента страницы
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


# Функция для извлечения данных со страницы категории
async def parse_category_page(session, category_url):
    books_data = []
    html = await fetch(session, category_url)
    soup = BeautifulSoup(html, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text.strip()
        in_stock = 'In stock' in book.find('p', class_='instock availability').text
        relative_link = book.h3.a['href']
        book_url = urljoin(category_url, relative_link)
        books_data.append({
            'Title': title,
            'Price': price,
            'In stock': in_stock,
            'Link': book_url,
        })

    # Проверяем наличие следующей страницы
    next_page_link = soup.select_one('li.next > a')
    next_page_url = urljoin(category_url, next_page_link['href']) if next_page_link else None

    return books_data, next_page_url


# Функция для извлечения детальных данных книги
async def parse_book_details(session, book_url):
    html = await fetch(session, book_url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='table table-striped')
    details = {row.th.text: row.td.text for row in table.find_all('tr')}

    return details


# Функция для записи данных в CSV
def save_to_csv(books, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)


# Основная функция для скрапинга
async def scrape_category(category_url):
    async with aiohttp.ClientSession() as session:
        all_books = []
        next_page_url = category_url

        while next_page_url:
            books, next_page_url = await parse_category_page(session, next_page_url)

            for book in books:
                details = await parse_book_details(session, book['Link'])
                book.update(details)
                all_books.append(book)

        csv_filename = 'books.csv'
        save_to_csv(all_books, csv_filename)
        return csv_filename


# Стартовый URL категории
category_url = 'https://books.toscrape.com/catalogue/category/books/fiction_10/index.html'

# Запуск асинхронной функции scrape_category
asyncio.run(scrape_category(category_url))

