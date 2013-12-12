# coding=utf-8
__author__ = 'jdayllon'

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest, HtmlResponse
from estado.items import FileItem, BidItem
from selenium import webdriver
from pyvirtualdisplay import Display
from scrapy import log
import re

class bidSpider(BaseSpider):
    name = "bid"
    allowed_domains = ["contrataciondelestado.es"]
    dont_filter = ["contrataciondelestado.es"]
    start_urls = [
        "https://contrataciondelestado.es/wps/portal/plataforma",
    ]

    SEEMORE_LINK = '//a[@alt="See more"]/@href'
    NEXTPAGE_LINK = '//div[@class="wpsPortletBody"]/form[@method="post"]/@action'
    NEXTPAGE_FIELD = '//input[@class="botonEnlace"]/@id'
    NEXTPAGE_VALUE = 'Next >>'
    NEXTPAGE_ID = '//div[@class="wpsPortletBody"]/form[@method="post"]/@id'

    FILE_LINK = '//span[starts-with(.,"File")]/..//a/@href'
    FILE_PUBLIC = '//span[starts-with(.,"File")]/..//a/text()'
    FILE_LASTUPDATE = '//span[starts-with(.,"File")]/..//a/../../../td[2]/span[2]/text()'
    FILE_TITLE = '//span[starts-with(.,"Contract Title")]/../span[not(starts-with(.,"Contract Title"))]/text()'
    FILE_CATEGORY = '//span[starts-with(.,"Category")]/../span[not(starts-with(.,"Category"))]/text()'
    FILE_PRESENTATION = '//span[starts-with(.,"Presentation end date")]/../span[not(starts-with(.,"Presentation end date"))]/text()'
    FILE_CONTRACTOR = '//span[starts-with(.,"Contracting agency")]/../span[not(starts-with(.,"Contracting agency"))]/text()'
    FILE_AMOUNT = '//span[starts-with(.,"Amount")]/../span[not(starts-with(.,"Amount"))]/text()'

    SEL_LINK = '//span[starts-with(.,"Expediente")]/..//a'
    SEL_PUBLIC = '//span[starts-with(.,"Expediente")]/..//a'
    SEL_LASTUPDATE = '//span[starts-with(.,"Expediente")]/..//a/../../../td[2]/span[2]'
    SEL_TITLE = '//span[starts-with(.,"Título")]/../span[not(starts-with(.,"Título"))]'
    SEL_CATEGORY = '//span[starts-with(.,"Categoría")]/../span[not(starts-with(.,"Categoría"))]'
    SEL_PRESENTATION = '//span[starts-with(.,"F. Fin de presentación")]/../span[not(starts-with(.,"F. Fin de presentación"))]'
    SEL_CONTRACTOR = '//span[starts-with(.,"Órgano de Contratación")]/../span[not(starts-with(.,"Órgano de Contratación"))]'
    SEL_AMOUNT = '//span[starts-with(.,"Importe")]/../span[not(starts-with(.,"Importe"))]'



    base_url_1 = ''
    base_url_2 = ''

    def __init__(self):
        log.msg("Inicializando Virtual Display", level=log.INFO)
        self.display = Display()
        self.display.start()

        log.msg("Inicializando Navegador", level=log.INFO)
        self.driver = webdriver.Firefox()

    def __del__(self):
        print self.verificationErrors
        CrawlSpider.__del__(self)
        log.msg("Finalizando Display", level=log.INFO)
        self.display.stop()
        log.msg("Finalizando Selenium", level=log.INFO)
        self.selenium.stop()

    def add_hostname(self, path):
        #print "ADD HOSTNAME: hostname %s" % path
        return "https://contrataciondelestado.es%s" % path

    def get_idbid(self,url):
        regex = 'idLicitacion=([\d-]{0,20})'
        return re.search(regex,url).group(1)

    def __set_base_url__(self,url):
        url_parts = url.split(self.get_idbid(url))
        self.base_url_1 = url_parts[0]
        self.base_url_2 = url_parts[1]

    def get_bid_url(self,bid):
        return "%s%s%s" % (self.base_url_1, bid, self.base_url_2)

    def parse(self, response):
        request = []

        sel = Selector(response)
        file_list_entries = sel.xpath(self.SEEMORE_LINK)

        for file_list_entry in file_list_entries:
            request.append(Request(self.add_hostname(file_list_entry.extract()), callback=self.parse_page_list))

        return request


    def parse_page_list(self, response):

        request = []
        bids = []
        first_page_flag = True
        page_counter = 0

        self.driver.get(response.url)

        while True:

            log.msg("Page_Request %s " % response.url, level=log.INFO)

            ids = self.driver.find_elements_by_xpath(self.SEL_LINK) # sel.xpath(self.FILE_LINK)
            public_ids = self.driver.find_elements_by_xpath(self.SEL_PUBLIC)
            lastupdates = self.driver.find_elements_by_xpath(self.SEL_LASTUPDATE)
            titles = self.driver.find_elements_by_xpath(self.SEL_TITLE)
            cats = self.driver.find_elements_by_xpath(self.SEL_CATEGORY)

            try:
                presentations = self.driver.find_elements_by_xpath(self.SEL_PRESENTATION)
            except:
                presentations = None


            contractors = self.driver.find_elements_by_xpath(self.SEL_CONTRACTOR)
            amounts = self.driver.find_elements_by_xpath(self.SEL_AMOUNT)

            for pos in range(len(ids)):
                curBid = BidItem()
                curBid['id'] = ids[pos].get_attribute("href")
                curBid['publicId'] = public_ids[pos].text
                curBid['lastupdate'] = lastupdates[pos].text
                curBid['title'] = titles[pos].text
                curBid['cat'] = cats[pos].text

                try:
                    if presentations != None:
                        curBid['presentation_date'] = presentations[pos].extract()
                except:
                    curBid['presentation_date'] = ''

                curBid['contractor'] = contractors[pos].text
                curBid['amount'] = amounts[pos].text

                print "Call: %s" % ids[pos].get_attribute("href")
                request.append(Request(ids[pos].get_attribute("href"), callback=self.parse_bid))

                bids.append(curBid)

            # Process next pages
            nextInputButton = self.driver.find_elements_by_xpath('//input[@class="botonEnlace"]')
            log.msg("Page Counter: %s" % page_counter, level=log.INFO)

            if first_page_flag:
                nextInputButton = nextInputButton[-1]
                first_page_flag = False
                nextInputButton.click()
                page_counter += 1
            else:
                if len(nextInputButton) == 2:
                    nextInputButton = nextInputButton[-1]
                    nextInputButton.click()
                    page_counter += 1
                else:
                    pass

        request.append(bids)

        log.msg("Finalizando Browser", level=log.INFO)
        self.driver.quit()

        return request



        #for site in sites:
        #    title = site.xpath('a/text()').extract()
        #    link = site.xpath('a/@href').extract()
        #    desc = site.xpath('text()').extract()
        #    print title, link, desc