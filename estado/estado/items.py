# coding=utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import couchdbkit

from scrapy.item import Item, Field
from couchdbkit import *

import datetime


class Bid(Document):

    def getItem(self):

        bidItem = BidItem()
        bidItem['publicId'] = self.id
        bidItem['lastupdate'] = self.lastupdate
        bidItem['title'] = self.title
        bidItem['cat'] = self.cat
        bidItem['presentation_date'] = self.presentation_date
        bidItem['contractor'] = self.contractor
        bidItem['amount'] = self.amount

        return bidItem

    id = StringProperty()
    publicId = StringProperty()
    lastupdate = DateTimeProperty()
    title = StringProperty()
    cat = StringProperty()
    presentation_date = DateTimeProperty()
    contractor = StringProperty()
    amount = FloatProperty()

class FileBid(Document):

    expediente = StringProperty()
    tipo = StringProperty()
    subtipo = StringProperty()
    titulo = StringProperty()
    importe = FloatProperty()
    lugar = StringProperty()
    contratante = StringProperty()
    procedimiento = StringProperty()
    cpv = StringProperty()
    clasificacion = StringProperty()
    adjudicacion = StringProperty()
    ficheros = DictProperty()


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
    ficheros = Field()

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



