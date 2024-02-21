import scrapy

class JumiaSpider(scrapy.Spider):
    name = "jumia"
    start_urls = ["https://www.jumia.co.ke/phones-tablets/"]

    def parse(self, response):
        if response.css("div.itm"):
            for item in response.css("div.itm"):
                yield self.parse_item(item)
        elif response.css("article.prd"):
            for item in response.css("article.prd"):
                yield self.parse_item(item)
        else:
            self.logger.warning("No items found on the page.")

        next_page = response.css("a.pg::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.info("No more pages left. Stopping execution.")

    def parse_item(self, item):
        return {
            "Product": item.css("div.name::text").get(),
            "Price": item.css("div.prc::text").get(),
        }
