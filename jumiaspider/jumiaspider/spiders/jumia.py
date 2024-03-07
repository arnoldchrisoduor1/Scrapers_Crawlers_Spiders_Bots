import scrapy
from scrapy import Spider, Request
from scrapy.crawler import CrawlerRunner
from scrapy.mail import MailSender
from datetime import datetime
import random
import logging
import twisted.internet.reactor
import sys
import os
from scrapy.settings import Settings
from twisted.internet import reactor


# Add the project directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from scrapy.settings import Settings

# Create and configure the settings object
settings = Settings()
settings.setmodule('jumiaspider.settings')

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

class JumiaSpider(scrapy.Spider):
    name = "jumia"
    allowed_domains = ["jumia.co.ke"]
    categories = [
        "electronics",
        "sporting-goods",
        "video-games",
        "home-office-appliances",
        "automobile",
        "baby-products",
        "books-movies-music",
        "computing",
        "category-fashion-by-jumia",
        "patio-lawn-garden",
        "groceries",
        "health-beauty",
        "home-office",
        "industrial-scientific",
        "livestock",
        "miscellaneous",
        "musical-instruments",
        "pet-supplies",
        "phones-tablets",
        "toys-games",
    ]

    user_agent_list = settings.get('USER_AGENT_LIST')

    def start_requests(self):
        base_url = "https://www.jumia.co.ke/"
        for category in self.categories:
            category_url = f"{base_url}{category}/"
            user_agent = random.choice(self.user_agent_list)
            request = scrapy.Request(category_url, self.parse)
            request.headers['User-Agent'] = user_agent
            yield request

    def parse(self, response):
        logger.info(f"Parsing {response.url}")
        for item in response.css("div.itm, article.prd"):
            yield {
                "product": item.css("div.name::text, h3.name::text").get(),
                "new_price": item.css("div.prc::text").get(),
                "old_price": item.css("div::attr(data-oprc), div.old::text").get(),
                "category": response.url.split("/")[-2],
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        next_page = response.css('a[aria-label="Next Page"]::attr(href)').get()
        if next_page is not None:
            user_agent = random.choice(self.user_agent_list)
            request = response.follow(next_page, callback=self.parse)
            request.headers['User-Agent'] = user_agent
            yield request

    def spider_closed(self, spider):
        logger.info("Spider Closed")
        stats = spider.crawler.stats.get_stats()
        logger.info(f"Total items scraped: {stats.get('item_scraped_count')}")
        logger.info(f"Start time: {stats.get('start_time')}")
        logger.info(f"Finish time: {stats.get('finish_time')}")

        mailer = MailSender(
            mail_host=settings.get('MAIL_HOST'),
            mail_port=settings.get('MAIL_PORT'),
            mail_user=settings.get('MAIL_USER'),
            mail_pass=settings.get('MAIL_PASS'),
            mail_from=settings.get('MAIL_FROM'),
        )
        subject = "Jumia Scraping Completed"
        body = f"Total items scraped: {stats.get('item_scraped_count')}\n"
        body += f"Start time: {stats.get('start_time')}\n"
        body += f"Finish time: {stats.get('finish_time')}\n"
        body += "Scraping logs are attached."
        mailer.send(
            to=settings.get('MAIL_TO'),
            subject=subject,
            body=body,
            attachs=[settings.get('LOG_FILE')]
        )

# Run the spiders in parallel
if not twisted.internet.reactor.running:
    runner = CrawlerRunner(settings)
    tasks = [runner.crawl(JumiaSpider) for _ in range(4)]
    reactor.run()
else:
    logger.error("Reactor is already running.")