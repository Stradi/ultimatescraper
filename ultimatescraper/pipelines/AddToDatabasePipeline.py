import peewee
import ultimatescraper.models as models
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from ultimatescraper.utils.database import (get_connection_args_for_peewee,
                                            get_database_name)


class AddToDatabasePipeline:
    def process_item(self, item, spider):
        database = peewee.MySQLDatabase(
            get_database_name(),
            **get_connection_args_for_peewee()
        )

        with database:
            adapter = ItemAdapter(item)
            try:
                self.create_comic(adapter.asdict())
                return item
            except Exception as e:
                raise DropItem(str(e))

    def create_comic(self, data):
        comic = models.ComicModel.create(
            name=data["name"],
            slug=data["slug"],
            is_completed=data["isCompleted"],
            release_date=data["releaseDate"],
            summary=data["summary"],
            cover_image=data["coverImage"],
        )

        for tag in data["tags"]:
            self.create_tag(tag, comic)

        for author in data["authors"]:
            self.create_author(author, comic)

        for issue in data["issues"]:
            self.create_issue(issue, comic)
        return comic

    def create_issue(self, issue_data, comic):
        issue = models.IssueModel.create(
            name=issue_data["name"],
            slug=issue_data["slug"],
            comic=comic
        )

        pages = models.PageModel.insert_many([
            {
                "url": image,
                "issue": issue
            } for image in issue_data["images"]
        ]).execute()

        return issue

    def create_tag(self, tag_data, comic):
        tag = models.TagModel.get_or_create(
            name=tag_data["name"],
            slug=tag_data["slug"]
        )

        models.ComicTagModel.create(
            comic=comic,
            tag=tag[0]
        )

        return tag[0]

    def create_author(self, author_data, comic):
        author = models.AuthorModel.get_or_create(
            name=author_data["name"],
            slug=author_data["slug"]
        )

        models.ComicAuthorModel.create(
            comic=comic,
            author=author[0]
        )

        return author[0]
