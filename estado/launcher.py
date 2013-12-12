__author__ = 'jdayllon'
from scrapy.cmdline import execute

execute(['scrapy','crawl','extendedBid','-o bids.json -t json'])