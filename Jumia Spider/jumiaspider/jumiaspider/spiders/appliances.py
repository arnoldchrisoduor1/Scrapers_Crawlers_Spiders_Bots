import scrapy

class JumiaAppliances(scrapy.Spider):
    name = "jumia_appliances"

    start_urls = ["https://www.jumia.co.ke/home-office-appliances/"]

    def parse(self, response):
        for item in response.css("div.itm"):
            yield {
                "products" : item.css("div.name::text").get(),
                "new_price" : item.css("div.prc::text").get(),
                "old_price" : item.css("div.prc::attr(data-oprc)").get()
            }
        next_page = response.css('a[aria-label="Next Page"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_next_page)

    def parse_next_page(self, response):
        for item in response.css("article.prd"):
            yield {
                "product" : item.css("div.info h3.name::text").get(),
                "old_price" : item.css("div.old::text").get(),
                "new_price" : item.css("div.prc::text").get(),
            }
        next_page = response.css('a[aria-label="Next Page"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_next_page)