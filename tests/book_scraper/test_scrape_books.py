"""
Test method scrape_books
"""

import json
from pathlib import Path
import pytest
from books_scraper import scraper

ROOT_PATH = str(Path(__file__).parent.parent)


@pytest.fixture
def _mock_scraper(requests_mock, mocker):
    """
    Args:
        requests_mock: response fixture
        mocker: fixture

    """
    with open(f"{ROOT_PATH}/fixtures/catalogue.html", "r", encoding="utf-8") as f:
        catalogue = f.read()

    with open(f"{ROOT_PATH}/fixtures/book.json", "r", encoding="utf-8") as f:
        book = json.load(f)

    requests_mock.get("http://books.toscrape.com/catalogue/page-1.html", text=catalogue)
    requests_mock.get(
        "http://books.toscrape.com/catalogue/page-2.html", status_code=404
    )
    mocker.patch("books_scraper.scraper.get_book_data", return_value=book)
    return scraper.scrape_books()


def test_books_type(_mock_scraper):
    """
    Tests returned type is a list.

    Args:
        _mock_scraper: fixture
    """
    books = _mock_scraper
    assert isinstance(books, list)


def test_books_len(_mock_scraper):
    """
    Tests returned list len is equal to 1.

    Args:
        _mock_scraper: fixture
    """
    books = _mock_scraper
    assert len(books) == 1


def test_book_type(_mock_scraper):
    """
    Tests returned book type is a dict.

    Args:
        _mock_scraper: fixture
    """
    books = _mock_scraper
    assert isinstance(books[0], dict)


def test_book_keys(_mock_scraper):
    """
    Tests returned book keys is a list of
    "title", "price", "available", "description", "product_information"

    Args:
        _mock_scraper: fixture
    """
    books = _mock_scraper
    assert list(books[0].keys()) == [
        "title",
        "price",
        "available",
        "description",
        "product_information",
    ]


def test_book_information_type(_mock_scraper):
    """
    Tests returned book information type is a dict.

    Args:
        _mock_scraper: fixture
    """
    books = _mock_scraper
    assert isinstance(books[0]["product_information"], dict)


def test_book_information_keys(_mock_scraper):
    """
    Tests returned book information keys is a list of
    "UPC", "Product Type", "Price (excl. tax)", "Price (incl. tax)",
    "Tax", "Availability", "Number of reviews"

    Args:
        _mock_scraper: fixture
    """
    books = _mock_scraper
    assert list(books[0]["product_information"].keys()) == [
        "UPC",
        "Product Type",
        "Price (excl. tax)",
        "Price (incl. tax)",
        "Tax",
        "Availability",
        "Number of reviews",
    ]
