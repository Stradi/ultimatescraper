import logging

import scrapy

from ultimatescraper.items import ComicItem

ALL_COMICS_URL = "https://viewcomics.me/comic-list"


class ViewcomicsSpider(scrapy.Spider):
    name = 'ViewComics'
    allowed_domains = ['viewcomics.me']
    start_url = ALL_COMICS_URL

    custom_settings = {
        'ITEM_PIPELINES': {
            'ultimatescraper.pipelines.PopulateItemsPipeline.ValidateItemPipeline': 100,
            'ultimatescraper.pipelines.AddToDatabasePipeline.AddToDatabasePipeline': 200,
        }
    }

    def __init__(self, comic=None, *args, **kwargs):
        if comic == None:
            self.start_url = ALL_COMICS_URL
        else:
            self.start_url = comic

        super(ViewcomicsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        if self.start_url == ALL_COMICS_URL:
            yield scrapy.Request(self.start_url, callback=self.parse_all_comics)
        else:
            yield scrapy.Request(self.start_url, callback=self.parse_comic)

    def parse_all_comics(self, response):
        urls_in_page = response.css('.line-list a::attr(href)').getall()
        next_page_url = response.css('a[rel=next]::attr(href)').get()

        for url in urls_in_page:
            yield scrapy.Request(url, callback=self.parse_comic)

        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_all_comics)

    def parse_comic(self, response):
        def parse_table():
            table_keys = response.css(
                '.full-table tr td:nth-child(1) *::text').getall()
            table_values = response.css(
                '.full-table tr td:nth-child(2) *::text').getall()

            return dict(zip(table_keys, table_values))

        table_data = parse_table()
        data = {
            'name': table_data['Name:'],
            'isCompleted': True if response.css('.status a::text').get().strip() == 'Ongoing' else False,
            'releaseDate': table_data['Year of Release:'].strip(),
            'summary': response.css('.detail-desc-content p::text').get().strip(),
            'tags': response.css('.anime-genres li:not(:nth-child(1)) a::text').getall(),
            'authors': [table_data['Author:'].strip()],
            '_issues': response.css('.basic-list a::attr(href)').getall(),
            "issues": []
        }

        # In here we are doing some kinda hack for scraping all the issues before
        # yielding the data.
        first_issue = data['_issues'].pop()
        yield response.follow("{url}/full".format(url=first_issue), callback=self.parse_issue, cb_kwargs={'data': data})

    def parse_issue(self, response, data):
        images = response.css('.chapter-container img::attr(src)').getall()
        issue_no = response.css('.title h1::text').get().split('#')[1]
        data["issues"].append({
            "number": issue_no,
            "images": images
        })

        # Try to get issue from arbitrary list. If we don't have any issues left
        # then that means that we scraped all the issues for this comic, so we
        # yield the data. Otherwise, we continue scraping the issues.
        try:
            next_issue_url = data['_issues'].pop()
        except IndexError:
            del data['_issues']
            logging.debug("Parsed {comicname} page, passing it to pipelines.".format(
                comicname=data['name']))
            yield ComicItem(**data)
        else:
            yield response.follow("{url}/full".format(url=next_issue_url), callback=self.parse_issue, cb_kwargs={'data': data})
