# Краулинг и парсинг каталога книг ресурса books.toscrape.com

## Цель проекта
Применить на практике базовые подходы к web-scraping с библиотеками requests и BeautisulSoup: навигация по страницам, извлечение HTML-элементов, парсинг.

## Инструкции по запуску
### Скачайте проект 
### Запустите виртуальное окружение 
`pipenv shell`
### Установите зависимости
`pip install -r requirements.txt`
### Запустите скрипт
`python3 -i ./src/books_scraper/scraper.py`

В логах вы увидете

```
Start scraping.
Scraping is finished. Checked 50 pages, archived 1000 books.The result saved to /artifacts/books_data.txt
```

### Сохранение результата

По умолчанию скрипт сохраняет список книг в `/artifacts/books_data.txt`

### Тесты
Для запуска тестов используйте
```
pytest tests/
```

## Список используемых библиотек
* pathlib
* re
* requests
* bs4
* json
* pytest