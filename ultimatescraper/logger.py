import logging

from scrapy import logformatter


class PrettyLogFormatter(logformatter.LogFormatter):
  def crawled(self, request, response, spider):
    return {
      'level': logging.DEBUG,
      'msg': "Crawled (%(status)s) <%(url)s>",
      'args': {
        'status': response.status,
        'url': request.url,
      }
    }

  def scraped(self, item, response, spider):
    return {
      'level': logging.INFO,
      'msg': "Scraped \"%(comicname)s\" with %(issues)s issues",
      'args': {
        'comicname': item["name"],
        'issues': len(item["issues"])
      }
    }

  def dropped(self, item, exception, response, spider):
    return {
      'level': logging.WARNING,
      'msg': "Dropped \"%(comicname)s\": %(exception)s",
      'args': {
        'comicname': item["name"],
        'exception': exception,
      }
    }

  def download_error(self, failure, request, spider, errmsg=None):
    return super().download_error(failure, request, spider, errmsg)

  def item_error(self, item, exception, response, spider):
    return super().item_error(item, exception, response, spider)

  def spider_error(self, failure, request, response, spider):
    return super().spider_error(failure, request, response, spider)

  
