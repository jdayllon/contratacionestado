# coding=utf-8
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

class BidItem(Item):
    """

    Example:
    File01/2013	Date of last update	16-11-2013 12:17
    Contract TitleRecogida de residuos sólidos urbanos del C.P. OCAÑA II
    CategoryServicios de recogida de desperdicios sólidos urbanos.
    Presentation end date26-11-2013 12:15:00
    Contracting agencyDirección del Centro Penitenciario Ocaña II
    Amount26,363.36
    """
    id = Field()
    publicId = Field()
    lastupdate = Field()
    title = Field()
    cat = Field()
    presentation_date = Field()
    contractor = Field()
    amount = Field()
