# coding=utf-8
__author__ = 'jdayllon'

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from estado.items import FileItem

class AdjudicaSpider(BaseSpider):
    name = "Adjudicaciones"
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

    FILE_XML_LINK = '//a[starts-with(.,"Xml")]/@href'
    FILE_FIELDS = "//input[@type='text']/@value"
    FILE_TEXTAREA = "//textarea/text()"

    def add_hostname(self, path):
        #print "add hostname %s" % path
        return "https://contrataciondelestado.es%s" % path

    def parse(self, response):
        request = []
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)

        sel = Selector(response)
        file_list_entries = sel.xpath(self.SEEMORE_LINK)

        for file_list_entry in file_list_entries:
            request.append(Request(self.add_hostname(file_list_entry.extract()), callback=self.parse_page_list))

        return request


    def parse_page_list(self, response):

        request = []

        print "Page_Request"

        sel = Selector(response)
        files = sel.xpath(self.FILE_LINK)

        #sel.xpath('//input[@class="botonEnlace"]')[0].extract()
        #sel.xpath('//div[@class="wpsPortletBody"]/form[@method="POST"]')

        #viewns_Z7_G064CI9300DE90IOTJRCT70OT7_:form1	viewns_Z7_G064CI9300DE90IOTJRCT70OT7_:form1

        # Process next pages
        form_id = sel.xpath(self.NEXTPAGE_ID)[0].extract()
        nextpage = sel.xpath(self.NEXTPAGE_LINK)[0].extract()
        idname_next_page_field = sel.xpath(self.NEXTPAGE_FIELD)[0].extract()

        #request.append(FormRequest(url=self.add_hostname(nextpage),
        #            formdata={idname_next_page_field: self.NEXTPAGE_VALUE, form_id: form_id},
        #            callback=self.parse_page_list))

        # Process individual files
        for file in files:
            request.append(Request(self.add_hostname(file.extract()), callback=self.parse_page))

        return request

    def parse_page(self, response):
        #print "salida"
        sel = Selector(response)

        current_file = FileItem()

        file_xml = sel.xpath(self.FILE_FIELDS)

        current_file['expediente'] = file_xml[0].extract()
        current_file['tipo'] = file_xml[1].extract()
        current_file['subtipo'] = file_xml[2].extract()
        current_file['importe'] = file_xml[3].extract()
        current_file['lugar'] = file_xml[4].extract()
        current_file['procedimiento'] = file_xml[5].extract()
        current_file['cpv'] = file_xml[6].extract()
        #current_file['clasificacion'] = file_xml[7].extract()
        #current_file['adjudicacion'] = file_xml[8].extract()

        file_text_xml = sel.xpath(self.FILE_TEXTAREA)

        current_file['titulo'] = file_text_xml[0].extract()
        current_file['contratante'] = file_text_xml[0].extract()

        return current_file

        #for site in sites:
        #    title = site.xpath('a/text()').extract()
        #    link = site.xpath('a/@href').extract()
        #    desc = site.xpath('text()').extract()
        #    print title, link, desc

    def download_xml(self,response):
        #path = self.get_path(response.url)
        #with open(path, "wb") as f:
        #f.write(response.body)
        pass