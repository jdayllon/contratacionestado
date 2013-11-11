__author__ = 'jdayllon'

from scrapy.spider import BaseSpider

class AdjudicaSpider(BaseSpider):
    name = "Adjudicaciones"
    allowed_domains = ["https://contrataciondelestado.es"]
    start_urls = [
        "https://contrataciondelestado.es",
    ]

    1ST_LINK = ""//a[@alt='Ver más']""

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)