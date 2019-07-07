# Scrapy settings for estado project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'estado'

SPIDER_MODULES = ['estado.spiders']
NEWSPIDER_MODULE = 'estado.spiders'
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 0.5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'estado (+http://www.yourdomain.com)'
