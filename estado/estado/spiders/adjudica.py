# coding=utf-8
__author__ = 'jdayllon'

from scrapy.spider import BaseSpider

class AdjudicaSpider(BaseSpider):
    name = "Adjudicaciones"
    allowed_domains = ["https://contrataciondelestado.es"]
    start_urls = [
        "https://contrataciondelestado.es/wps/portal/plataforma",
    ]

    SEEMORE_LINK = '//a[@alt="See more"]/@href'

    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)

        sel = Selector(response)
        contracts = sel.xpath(self.SEEMORE_LINK)[1]
        Request("https://contrataciondelestado.es%s" % contracts.extract(), callback=self.parse)


    def parse_page_list(self, response):

        sel = Selector(response)


        #for site in sites:
        #    title = site.xpath('a/text()').extract()
        #    link = site.xpath('a/@href').extract()
        #    desc = site.xpath('text()').extract()
        #    print title, link, desc