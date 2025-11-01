"""
Test method get_book_data
"""

from pathlib import Path
from books_scraper import scraper

ROOT_PATH = str(Path(__file__).parent.parent)


def test_get_book_data(requests_mock):
    """
    Tests returned type is a dict.

    Args:
        requests_mock: fixture
    """

    book_url = (
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )
    with open(f"{ROOT_PATH}/fixtures/book.html", "r", encoding="utf-8") as f:
        book = f.read()
    requests_mock.get(book_url, text=book)
    book = scraper.get_book_data(book_url=book_url)
    assert isinstance(book, dict)
