# coding=utf-8
__author__ = 'jdayllon'

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from estado.items import FileItem, BidItem, FileBid
from idBid import bidSpider
from scrapy import log
import re


class extendedBidSpider(bidSpider):
    # Constantes
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


    def parse_bid(self, response):
        """
        Carga el contenido de una licitacion de contratacion del estado
        @param response:
        @return:
        """
        sel = Selector(response)
        current_file = FileItem()
        FileBid.set_db(self.db)
        fileBid = FileBid()

        file_basic_data = sel.xpath(self.FILE_FIELDS)

        #Se extraen los datos basicos del expediente
        log.msg("Bid: %s" % file_basic_data[0].extract(), level=log.DEBUG)

        xml_files_url = sel.xpath(self.FILE_XML_LINK).extract()
        xml_files_type = sel.xpath(self.FILE_XML_LINK_TYPE).extract()
        file_extended_data = sel.xpath(self.FILE_TEXTAREA)

        current_file['ficheros'] = ''

        xml_files = dict(zip(xml_files_type, xml_files_url))

        fileBid.expediente = file_basic_data[0].extract()
        fileBid.tipo = file_basic_data[1].extract()
        fileBid.subtipo = file_basic_data[2].extract()
        fileBid.titulo = file_extended_data[0].extract()
        fileBid.importe = float(numbers.parse_decimal(file_basic_data[3].extract()))
        fileBid.lugar = file_basic_data[4].extract()
        fileBid.contratante = file_extended_data[0].extract()
        fileBid.procedimiento = file_basic_data[5].extract()
        fileBid.cpv = file_basic_data[6].extract()
        #fileBid.clasificacion = StringProperty()
        #fileBid.adjudicacion = StringProperty()
        fileBid.ficheros = xml_files

        fileBid.save()

        current_file['expediente'] = file_basic_data[0].extract()
        current_file['tipo'] = file_basic_data[1].extract()
        current_file['subtipo'] = file_basic_data[2].extract()
        current_file['importe'] = file_basic_data[3].extract()
        current_file['lugar'] = file_basic_data[4].extract()
        current_file['procedimiento'] = file_basic_data[5].extract()
        current_file['cpv'] = file_basic_data[6].extract()
        #current_file['clasificacion'] = file_basic_data[7].extract()
        #current_file['adjudicacion'] = file_basic_data[8].extract()

        current_file['titulo'] = file_extended_data[0].extract()
        current_file['contratante'] = file_extended_data[0].extract()

        for xml_file in xml_files:
            filename = "%s_%s" % (current_file['expediente'], xml_file )
            filename = re.sub(r'\W+', '', filename)
            log.msg("Bid: %s - %s " % (file_basic_data[0].extract(), filename), level=log.DEBUG)
            #Concatena los diferentes ficheros para un proceso posterior
            current_file['ficheros'] = "%s;%s" % (current_file['ficheros'], filename)

        return current_file
