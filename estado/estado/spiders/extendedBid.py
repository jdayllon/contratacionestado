# coding=utf-8
__author__ = 'jdayllon'

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from estado.items import FileItem, BidItem
from idBid import bidSpider
#import pycurl
import re

class extendedBidSpider(bidSpider):
    name = "extendedBid"
    CHROME_PATH = 'path\to\chromedriver_win32_2.0'
    allowed_domains = ["contrataciondelestado.es"]
    dont_filter = ["contrataciondelestado.es"]
    start_urls = [
        "https://contrataciondelestado.es/wps/portal/plataforma",
    ]


    FILE_XML_LINK = '//a[starts-with(.,"Xml")]/@href'
    FILE_XML_LINK_TYPE = '//td[contains(@class, "tipoDocumento")]/div/text()'
    FILE_FIELDS = "//input[@type='text']/@value"
    FILE_TEXTAREA = "//textarea/text()"



    def download_xml(self,response):
        #path = self.get_path(response.url)
        #with open(path, "wb") as f:
        #f.write(response.body)
        pass

    def parse_page(self, response):
        #print "salida"

        sel = Selector(response)

        current_file = FileItem()

        file_basic_data = sel.xpath(self.FILE_FIELDS)

        current_file['expediente'] = file_basic_data[0].extract()
        current_file['tipo'] = file_basic_data[1].extract()
        current_file['subtipo'] = file_basic_data[2].extract()
        current_file['importe'] = file_basic_data[3].extract()
        current_file['lugar'] = file_basic_data[4].extract()
        current_file['procedimiento'] = file_basic_data[5].extract()
        current_file['cpv'] = file_basic_data[6].extract()
        #current_file['clasificacion'] = file_basic_data[7].extract()
        #current_file['adjudicacion'] = file_basic_data[8].extract()

        file_extended_data = sel.xpath(self.FILE_TEXTAREA)

        current_file['titulo'] = file_extended_data[0].extract()
        current_file['contratante'] = file_extended_data[0].extract()


        xml_files_url = sel.xpath(self.FILE_XML_LINK).extract()
        xml_files_type = sel.xpath(self.FILE_XML_LINK_TYPE).extract()

        xml_files = dict(zip(xml_files_type, xml_files_url))

        for xml_file in xml_files:
            #yield self.download_xml(current_file['expediente'], xml_file, xml_files[xml_file])
            filename = "%s_%s" % (current_file['expediente'], xml_file )
            filename = re.sub(r'\W+', '', filename)
            filename = "%s.xml" % filename
            #fp = open(filename, "wb")
            #curl = pycurl.Curl()
            #curl.setopt(pycurl.URL, str(xml_files[xml_file]))
            #curl.setopt(pycurl.WRITEDATA, fp)
            #curl.setopt(pycurl.SSL_VERIFYPEER, 0)
            #curl.setopt(pycurl.SSL_VERIFYHOST, 0)
            #curl.setopt(pycurl.FOLLOWLOCATION,1)
            #curl.perform()
            #curl.close()
            #fp.close()


        return current_file
