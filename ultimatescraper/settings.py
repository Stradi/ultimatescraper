BOT_NAME = 'ultimatescraper'
USER_AGENT = 'UltimateComic/0.1.0 (+https://www.ultimatecomic.com)'

CONCURRENT_REQUESTS = 32
TELNETCONSOLE_ENABLED = False
ROBOTSTXT_OBEY = False

SPIDER_MODULES = ['ultimatescraper.spiders']
NEWSPIDER_MODULE = 'ultimatescraper.spiders'

LOG_FORMATTER = 'ultimatescraper.logger.PrettyLogFormatter'
LOG_FORMAT = '%(asctime)s [%(levelname)8s]: %(message)s'
LOG_DATEFORMAT = '%y-%m-%d %H:%M:%S'
LOG_LEVEL = 'INFO'

ITEM_PIPELINES = {
   'ultimatescraper.pipelines.ValidateItemPipeline.ValidateItemPipeline': 100,
   'ultimatescraper.pipelines.AddToDatabasePipeline.AddToDatabasePipeline': 200,
}
