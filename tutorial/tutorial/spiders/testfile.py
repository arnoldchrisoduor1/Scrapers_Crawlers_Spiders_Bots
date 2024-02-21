# Scraping the Jumia website

import scrapy

class JumiaSpider(scrapy.Spider):
    name = "jumia"

    start_urls = ["https://www.jumia.co.ke/phones-tablets/"]

    def parse(self, response):
        count = 0
        for item in response.css("div.itm"):
            yield {
                "Product": item.css("div.name::text").get(),
                "Price": item.css("div.prc::text").get(),
            }

        next_page = response.css("a.pg::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_second_page)

    def parse_second_page(self, response):
        for item in response.css("article.prd"):
            yield {
                "Product": item.css("div.info h3.name::text").get(),
                "Price" : item.css("div.info div.prc::text").get(),
            }

        third_page = response.css("a.pg::attr(href)").get()
        if third_page:
            yield response.follow(third_page, callback=self.parse_third_page)

    def parse_third_page(self, response):
        for item in response.css("article.prd"):
            yield{
                "Product": item.css("div.info h3.name::text").get(),
                "Price": item.css("div.info div.prc::text").get(),
            }

        fourth_page = response.css("a.pg::attr(href)").get()
        if fourth_page:
                yield response.follow(fourth_page, callback=self.parse_fourth_page)

    def parse_fourth_page(self, response):
        for item in response.css("article.prd"):
            yield{
                "Product": item.css("div.info h3.name::text").get(),
                "Price": item.css("div.info div.prc::text").get(),
            }
