import scrapy

class JumiaSpider(scrapy.Spider):
    name = "jumia"

    start_urls = ["https://www.jumia.co.ke/phones-tablets/"]

    def parse(self, response):
        for item in response.css("div.itm"):
            yield {
                "products" : item.css("div.name::text").get(),
                "price" : item.css("div.prc::text").get(),
            }

        next_page = response.css('a[aria-label="Next Page"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_first_page)

    def parse_first_page(self, response):
        for item in response.css("article.c-prd"):
            yield {
                "product" : item.css("div.info h3.name::text").get(),
                "old price" : item.css("div.old::text").get(),
                "new price" : item.css("div.prc::text").get(),
            }
            next_page = next_page = response.css('a[aria-label="Next Page"]::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_first_page)

