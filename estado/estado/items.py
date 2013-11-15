# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class FileItem(Item):
    # define the fields for your item here like:
    # name = Field()
    expediente = Field()
    tipo = Field()
    subtipo = Field()
    titulo = Field()
    importe = Field()
    lugar = Field()
    contratante = Field()
    procedimiento = Field()
    cpv = Field()
    clasificacion = Field()
    adjudicacion = Field()
