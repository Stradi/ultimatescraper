import os

from dotenv import load_dotenv

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

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_SSL_CERT = os.environ.get("DB_SSL_CERT")
REVALIDATION_SECRET = os.environ.get("REVALIDATION_SECRET")
REVALIDATION_URL = os.environ.get("REVALIDATION_URL")