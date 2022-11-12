import peewee
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import ultimatescraper.models as models
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
        try:
            comic = models.ComicModel.get(models.ComicModel.slug == data["slug"])

            for tag in data["tags"]:
                self._create_tag_impl(tag, comic)
            
            for author in data["authors"]:
                self._create_author_impl(author, comic)
            
            for issue in data["issues"]:
                self.create_issue(issue, comic)

        except models.ComicModel.DoesNotExist:
            return self._create_comic_impl(data)

    def create_issue(self, issue, comic):
        try:
            issue = models.IssueModel.select().join(models.ComicModel).where(
                models.IssueModel.slug == issue["slug"], models.ComicModel.slug == comic.slug).get()
        except models.IssueModel.DoesNotExist:
            return self._create_issue_impl(issue, comic)

    def _create_comic_impl(self, data):
        comic = models.ComicModel.create(
            name=data["name"],
            slug=data["slug"],
            is_completed=data["isCompleted"],
            release_date=data["releaseDate"],
            summary=data["summary"],
            cover_image=data["coverImage"],
        )

        for tag in data["tags"]:
            self._create_tag_impl(tag, comic)

        for author in data["authors"]:
            self._create_author_impl(author, comic)

        for issue in data["issues"]:
            self._create_issue_impl(issue, comic)
        return comic

    def _create_issue_impl(self, issue_data, comic):
        issue = models.IssueModel.create(
            name=issue_data["name"],
            slug=issue_data["slug"],
            comic=comic
        )

        models.PageModel.insert_many([
            {
                "url": image,
                "issue": issue
            } for image in issue_data["images"]
        ]).execute()

        return issue

    def _create_tag_impl(self, tag_data, comic):
        tag = models.TagModel.get_or_create(
            name=tag_data["name"],
            slug=tag_data["slug"]
        )

        models.ComicTagModel.create(
            comic=comic,
            tag=tag[0]
        )

        return tag[0]

    def _create_author_impl(self, author_data, comic):
        author = models.AuthorModel.get_or_create(
            name=author_data["name"],
            slug=author_data["slug"]
        )

        models.ComicAuthorModel.create(
            comic=comic,
            author=author[0]
        )

        return author[0]