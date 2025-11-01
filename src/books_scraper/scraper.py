"""
Script for scrapping books catalog from "http://books.toscrape.com/catalogue/"
"""

from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup

ROOT_PATH = str(Path(__file__).parent.parent.parent)


def get_book_data(book_url: str) -> dict:
    """
    Parse book data from book_url

    Args:
        book_url: url to get a book

    Returns:
        book info dictionary

    """
    page = requests.get(book_url, timeout=60)
    page.raise_for_status()
    page.encoding = "utf-8"
    soup = BeautifulSoup(page.text, "html.parser")
    result = {}

    try:
        result["title"] = soup.find("h1").get_text()
    except AttributeError:
        result["title"] = "not found"
    try:
        result["price"] = soup.find("p", attrs={"class": "price_color"}).get_text()
    except AttributeError:
        result["price"] = "not found"
    try:
        result["available"] = re.search(
            r"\d+", soup.find("p", attrs={"class": "instock availability"}).get_text()
        ).group(0)
    except AttributeError:
        result["available"] = "not found"
    try:
        result["description"] = (
            soup.find("div", attrs={"id": "product_description"}).find_next_sibling("p")
        ).get_text()
    except AttributeError:
        result["description"] = "not found"
    try:
        product_information = {}
        for tr in soup.find("table").find_all("tr"):
            product_information[tr.find("th").get_text()] = tr.find("td").get_text()
        result["product_information"] = product_information
    except AttributeError:
        result["product_information"] = {}

    return result


def scrape_books(is_save: bool = True, filename: str = "books_data.txt") -> list:
    """
    Parse books list, put information about books to file

    Args:
        is_save: sign if the result should be saved
        filename: filename for the result saving

    Returns:
        list of books

    """
    print("Start scraping.")
    root = "http://books.toscrape.com/catalogue/"
    i = 0
    result = []

    while True:
        i += 1
        page_url = re.sub(r"{N}", str(i), root + "page-{N}.html")
        response = requests.get(page_url, timeout=60)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        books_soup = soup.find("ol").find_all("li")
        for book in books_soup:
            book_link = book.find("a")
            if book_link.has_attr("href"):
                href = book_link["href"]
                try:
                    book_data = get_book_data(root + href)
                except AttributeError as e:
                    print(f"get_book_data({root + href})." f"ERROR: {e}")
                    continue
                result.append(book_data)

    if is_save:
        with open(f"{ROOT_PATH}/artifacts/{filename}", "w", encoding="utf-8") as f:
            f.write("\n".join(str(result)))
    print(
        "Scraping is finished. "
        f"Checked {i - 1} pages, archived {len(result)} books."
        f"The result saved to {f"/artifacts/{filename}"}"
    )
    return result


if __name__ == "__main__":
    try:
        scrape_books()
    except AttributeError as e:
        print("scrape_books() raise the ERROR: " f"{e}")
