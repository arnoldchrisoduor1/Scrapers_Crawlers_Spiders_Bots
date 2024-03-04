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
        next_page = response.css("a.pg svg.ic::attr(href)").get()
        if next_page():
            yield response.follow(next_page, callback = self.parse_next_page)

    def parse_next_page(self, response):
        for item in response.css("article.prd"):
            yield {
                "product" : item.css("div.name::text").get(),
                "old price": item.css("div.old::text").get(),
                "new price": item.css("div.prc").get(),
                "percentage change": item.css("div.bdg::text").get(),
            }