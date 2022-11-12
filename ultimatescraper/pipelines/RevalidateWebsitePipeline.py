import logging

import requests
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings

_PROJECT_SETTINGS = get_project_settings()

class RevalidateWebsitePipeline:
    session = None
    def process_item(self, item, spider):
        if self.session == None:
            self.session = requests.Session()

        adapter = ItemAdapter(item)

        urls_to_revalidate = []
        
        urls_to_revalidate.append("/comic/{}".format(adapter["slug"]))
        for issue in adapter["issues"]:
            urls_to_revalidate.append("/comic/{}/{}".format(adapter["slug"], issue["slug"]))

        for tag in adapter["tags"]:
            urls_to_revalidate.append("/tag/{}".format(tag["slug"]))

        for author in adapter["authors"]:
            urls_to_revalidate.append("/author/{}".format(author["slug"]))

        logging.info("Revalidating {} paths for {}".format(len(urls_to_revalidate), adapter["name"]))
        validated_paths, unvalidated_paths = self.revalidate_multiple(urls_to_revalidate)
        logging.info("Revalidated {}/{} paths for {}".format(len(validated_paths), len(unvalidated_paths), adapter["name"]))
        
        return item
        
    def revalidate_multiple(self, paths):
        full_url = "{}?secret={}".format(_PROJECT_SETTINGS.get('REVALIDATION_URL'), _PROJECT_SETTINGS.get('REVALIDATION_SECRET'))
        
        for path in paths:
            full_url += "&path={}".format(path)

        response = self.session.get(full_url)
        json = response.json()["data"]

        validated_paths = json["validatedPaths"]
        unvalidated_paths = json["notValidatedPaths"]

        return validated_paths, unvalidated_paths