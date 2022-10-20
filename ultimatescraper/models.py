import datetime
import os
from datetime import datetime

import peewee
from dotenv import load_dotenv

load_dotenv()

connection = peewee.MySQLDatabase(
  os.getenv("DATABASE"),
  host=os.getenv("HOST"),
  user=os.getenv("USER"),
  password=os.getenv("PASSWORD"),
  ssl_ca="{cwd}/{cert}".format(cwd=os.getcwd(), cert=os.getenv("SSL_CERT"))
)

class MetaModel(peewee.Model):
  id = peewee.AutoField(primary_key=True)
  created_at = peewee.DateTimeField(default=datetime.now)
  updated_at = peewee.DateTimeField(default=datetime.now)
  
  class Meta:
    database = connection

class BaseModel(MetaModel):
  name = peewee.CharField(255)
  slug = peewee.CharField(255)

class ComicModel(BaseModel):
  is_completed = peewee.BooleanField()
  release_date = peewee.DateField()
  summary = peewee.TextField()
  cover_image = peewee.TextField()
  class Meta:
    db_table = "comic"

class IssueModel(BaseModel):
  comic = peewee.ForeignKeyField(ComicModel, backref="issues", _deferred=True)
  class Meta:
    db_table = "issue"

class PageModel(MetaModel):
  issue = peewee.ForeignKeyField(IssueModel, backref="pages", _deferred=True)
  url = peewee.TextField()
  class Meta:
    db_table = "page"

class TagModel(BaseModel):
  class Meta:
    db_table = "tag"

class ComicTagModel(MetaModel):
  comic = peewee.ForeignKeyField(ComicModel, _deferred=True)
  tag = peewee.ForeignKeyField(TagModel, _deferred=True)
  class Meta:
    db_table = "comic_tag"

class AuthorModel(BaseModel):
  class Meta:
    db_table = "author"

class ComicAuthorModel(MetaModel):
  comic = peewee.ForeignKeyField(ComicModel, _deferred=True)
  author = peewee.ForeignKeyField(AuthorModel, _deferred=True)
  class Meta:
    db_table = "comic_author"

connection.connect()

connection.create_tables([
  ComicModel,
  IssueModel,
  PageModel,
  TagModel,
  AuthorModel,
  ComicTagModel,
  ComicAuthorModel
])

connection.close()
