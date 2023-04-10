import logging

import scrapy

# NOTE: Currently this scraper doesn't work since `readcomiconline.li` has a
# bot protection. We should find a way to bypass it. But it's a great start.

ALL_COMICS_URL = "https://readcomiconline.li/ComicList"
LATEST_COMICS_URL = "https://readcomiconline.li/ComicList/LatestUpdate"

CUSTOM_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"

class ReadComicOnlineSpider(scrapy.Spider):
    name = 'ReadComicOnline'
    allowed_domains = ['readcomiconline.li']
    start_url = ALL_COMICS_URL

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'ultimatescraper.pipelines.ValidateItemPipeline.ValidateItemPipeline': 100,
            # 'ultimatescraper.pipelines.AddToDatabasePipeline.AddToDatabasePipeline': 200,
            # 'ultimatescraper.pipelines.RevalidateWebsitePipeline.RevalidateWebsitePipeline': 300
        },
        'USER_AGENT': CUSTOM_USER_AGENT
    }

    def __init__(self, latest=None, comic=None, *args, **kwargs):
        super(ReadComicOnlineSpider, self).__init__(*args, **kwargs)

        if latest == None and comic == None:
            logging.info("No arguments passed, scraping all comics.")
            self.start_url = ALL_COMICS_URL
        elif latest == None and not comic == None:
            logging.info("Scraping comic '{comic_url}'".format(comic_url=comic))
            self.start_url = comic
        elif not latest == None and comic == None:
            logging.info("Scraping latest comics.")
            self.start_url = LATEST_COMICS_URL
        else:
            raise Exception(
                "You can't use both 'latest' and 'comic' arguments at the same time.")

    def start_requests(self):
        if self.start_url == LATEST_COMICS_URL:
            yield scrapy.Request(self.start_url, cookies={'list-view': 'list'}, callback=self.parse_latest_comics)
        elif self.start_url == ALL_COMICS_URL:
            yield scrapy.Request(self.start_url, callback=self.parse_all_comics)
        else:
            yield scrapy.Request(self.start_url, callback=self.parse_comic)

    def parse_latest_comics(self, response):
        found_any_comics = False

        all_items = response.css('.listing td:nth-child(1)')
        for item in all_items:
            url = item.css('a::attr(href)').get()
            all_banners = item.css('img::attr(title)').getall()
            for banner in all_banners:
                if banner == 'Just updated':
                    found_any_comics = True
                    yield response.follow(url, callback=self.parse_comic)

        if found_any_comics:
            pagination_urls = response.css('.pager a')
            for url in pagination_urls:
                next_page_url = url.css('*::attr(href)').get()
                if url.css('*::text').get() == '› Next ':
                    yield response.follow(next_page_url, callback=self.parse_latest_comics)

    def parse_all_comics(self, response):
        pass

    def parse_comic(self, response):
        def parse_info_box():
            items = response.css('.barContent p')
            full_info_box = {}

            for item in items:
                raw = item.css('*::text').getall()
                stripped = [r.strip() for r in raw]
                filter_pass = list(filter(None, stripped))
                final = list(filter((',').__ne__, filter_pass))

                key = final.pop(0)
                if len(final) == 0:
                    break

                full_info_box[key] = final

            return full_info_box

        info_dom = response.css('.barContent')
        info_box = parse_info_box()

        data = {
            'name': info_dom.css('.bigChar::text').get(),
            'isCompleted': True if info_box["Status:"][0] == "Completed" else False, 
            'releaseDate': info_box["Publication date:"][0],
            'summary': info_dom.css('p:last-child::text').get(),
            'tags': info_box["Genres:"],
            'authors': info_box['Writer:'] + info_box['Artist:'],
            '_issues': response.css('.listing tr a::attr(href)').getall(),
            'issues': []
        }

        first_issue = data['_issues'].pop()
        yield response.follow(first_issue, callback=self.parse_issue, cb_kwargs={'data': data})

    def parse_issue(self, response):
        pass
