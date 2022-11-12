import logging

import scrapy

from ultimatescraper.items import ComicItem


class ViewComicsLatestSpider(scrapy.Spider):
    name = 'ViewComicsLatest'
    allowed_domains = ['viewcomics.me']
    start_urls = ['https://viewcomics.me/comic-updates']

    custom_settings = {
        'ITEM_PIPELINES': {
            'ultimatescraper.pipelines.ValidateItemPipeline.ValidateItemPipeline': 100,
            'ultimatescraper.pipelines.AddToDatabasePipeline.AddToDatabasePipeline': 200,
            'ultimatescraper.pipelines.RevalidateWebsitePipeline.RevalidateWebsitePipeline': 300
        }
    }

    def parse(self, response):
        found_any_comics = False

        all_items = response.css('.line-list')
        for item in all_items:
            date = item.css('.date::text').get()
            if not (date == 'Today' or date == 'Yesterday'):
                continue

            found_any_comics = True

            url = item.css(':scope > li > a::attr(href)').get()
            yield response.follow(url, callback=self.parse_comic)
            # TODO: Check for '.icon-new'.

        if found_any_comics:
            next_page_url = response.css('a[rel=next]::attr(href)').get()
            yield response.follow(next_page_url, callback=self.parse)

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
