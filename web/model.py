"""Model classes."""

import markdown
import dateparser
from datetime import datetime


class Article:
    """Article on blog."""

    def __init__(self, stub):
        self.stub = stub
        self.publish_time = None
        self._meta_title = None
        self._meta_description = None
        self._content = None
        self._title = None
        self._abstract = None

    @property
    def is_published(self):
        """True if article is published."""
        return self.publish_time and self.publish_time <= datetime.now()

    @property
    def title(self):
        """Name of the article."""
        return self._title or ''

    @title.setter
    def set_title(self, value):
        """Sets name of the article."""
        self._title = value

    @property
    def meta_title(self):
        """Meta title of the article."""
        return self._meta_title or self.title

    @meta_title.setter
    def set_meta_title(self, value):
        """Sets meta title of the article."""
        self._meta_title = value

    @property
    def meta_description(self):
        """Meta description of the article."""
        return self._meta_description or self._abstract

    @meta_description.setter
    def set_meta_description(self, value):
        """Sets meta title of the article."""
        self._meta_description = value

    @property
    def content_html(self):
        """Main content of the article as html."""
        return markdown.markdown(self._content)

    @property
    def abstract_html(self):
        """Abstract of the article as html."""
        return markdown.markdown(self._abstract)

    @classmethod
    def from_json(cls, data):
        """Loads article from json data."""
        article = cls(data['stub'])
        article._meta_title = data['meta_title']
        article._meta_description = data['meta_description']
        article._content = data['content']
        article._title = data['title']
        article._abstract = data['abstract']
        article.publish_time = dateparser.parse(data['publish_time'])
        return article
