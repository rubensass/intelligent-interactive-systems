import os
from sys import path
import json

import scrapy
from scrapy.crawler import CrawlerProcess

path.append(os.getcwd())

from model.books_items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]
    file_path = "data.json"

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            relative_url = book.css("h3 a ::attr(href)").get()

            if "catalogue/" in relative_url:
                book_url = "https://books.toscrape.com/" + relative_url
            else:
                book_url = "https://books.toscrape.com/catalogue/" + relative_url
            yield response.follow(book_url, callback=self.parse_book_page)

        next_page = response.css("li.next a ::attr(href)").get()
        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):

        table_rows = response.css("table tr")

        url = response.url
        title = response.css(".product_main h1::text").get()
        availability = table_rows[5].css("td ::text").get()
        book_rating = response.css("p.star-rating").attrib["class"]
        rating_map = {
            "One": "20/100",
            "Two": "40/100",
            "Three": "60/100",
            "Four": "80/100",
            "Five": "100/100",
        }
        book_rating = rating_map[book_rating.split(" ")[-1]]
        category = response.xpath(
            "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
        ).get()
        description = response.xpath(
            "//div[@id='product_description']/following-sibling::p/text()"
        ).get()
        price = response.css("p.price_color ::text").get()
        price = price[1:] + " Dollars"

        book_item = BookItem(
            url=url,
            title=title,
            availability=availability,
            book_rating=book_rating,
            category=category,
            description=description,
            price=price,
        )

        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r") as json_file:
                my_list = json.load(json_file)
        else:
            my_list = []

        my_list.append(book_item.__dict__)

        with open(self.file_path, "w", encoding="utf-8") as json_file:
            json.dump(my_list, json_file, indent=4)

        yield book_item


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(BookspiderSpider)
    process.start()
