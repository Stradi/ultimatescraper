import logging
from datetime import datetime

import requests
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from slugify import slugify


class ValidateItemPipeline:
    session = None

    def process_item(self, item, spider):
        if self.session == None:
            self.session = requests.Session()

        adapter = ItemAdapter(item)

        valid_issues = []
        for issue in adapter["issues"]:
            issue["name"] = "Issue #{number}".format(number=issue["number"])
            
            # Ideally we should do any computation after validating the issue but in here
            # we assign slug because in some rare cases (I mean really rare) the slug
            # is not assigned and item still gets passed to the next pipeline. I don't
            # know why this happens but I'm think it's a bug in Scrapy or I am stupid.
            issue["slug"] = self.generate_slug(issue["name"])

            if not self.is_image_valid(issue["images"][0]):
                logging.debug("Skipping \"{issue}\" of \"{comicname}\" because images is invalid.".format(
                    issue=issue["name"], comicname=adapter["name"]))
                continue


            issue["images"] = [image.replace(
                "=s1600", "=s0") for image in issue["images"]]
            del issue["number"]
            valid_issues.append(issue)

        if len(valid_issues) <= 0:
            raise DropItem("All issues are invalid.")

        adapter["slug"] = self.generate_slug(adapter["name"])
        adapter["releaseDate"] = self.convert_to_date(adapter["releaseDate"])
        adapter["tags"] = [
            {"name": tag, "slug": self.generate_slug(tag)} for tag in adapter["tags"]]
        adapter["authors"] = [{"name": author, "slug": self.generate_slug(
            author)} for author in adapter["authors"]]
        adapter["summary"] = "" if adapter["summary"] == "N/a" else adapter["summary"]

        adapter["coverImage"] = adapter["issues"][0]["images"][0]

        del adapter["issues"]
        adapter["issues"] = valid_issues
        return item

    def generate_slug(self, name):
        return slugify(name)

    def convert_to_date(self, dateStr):
        return datetime(int(dateStr), 1, 1)

    def is_image_valid(self, image_url):
        resp = self.session.get(image_url.replace("=s1600", "=s1"))
        return resp.ok
