import scrapy


class ComicItem(scrapy.Item):
  name = scrapy.Field()
  slug = scrapy.Field()
  isCompleted = scrapy.Field()
  releaseDate = scrapy.Field()
  coverImage = scrapy.Field()
  summary = scrapy.Field()
  tags = scrapy.Field()
  authors = scrapy.Field()
  issues = scrapy.Field()
