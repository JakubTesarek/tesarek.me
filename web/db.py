"""Database driver."""

import boto3
import json
from web.model import Article


class Db:
    """S3 Database driver."""

    article_folder = 'articles'

    def __init__(self, conf):
        self.bucket = conf['bucket']
        self.client = self.connect(conf)

    def connect(self, conf):
        """Connect to S3 using provided credentials."""
        return boto3.client(
            's3',
            aws_access_key_id=conf['access_key_id'],
            aws_secret_access_key=conf['access_key_secret']
        )

    def find_article(self, stub):
        """Find article by stub."""
        return self._load_article(f'{self.article_folder}/{stub}.json')

    def _load_article(self, key):
        """Load article from database."""
        try:
            data = self._load_json_data(key)
            return Article.from_json(data)
        except self.client.exceptions.NoSuchKey:
            return None

    def find_articles(self, drafts=False):
        """Find all articles."""
        articles = []
        for key in self._list_keys(f'{self.article_folder}/'):
            article = self._load_article(key)
            if drafts or article.is_published:
                articles.append(article)
        articles.sort(key=lambda article: article.publish_time)
        return articles

    def _load_json_data(self, key):
        """Load data from S3 as dict."""
        result = self.client.get_object(Bucket=self.bucket, Key=key)
        text = result['Body'].read().decode()
        return json.loads(text)

    def _list_keys(self, prefix):
        """Get list of all keys with given prefix."""
        keys = []
        result = self.client.list_objects_v2(
            Bucket=self.bucket,
            Prefix=prefix
        )
        for item in result['Contents']:
            keys.append(item['Key'])
        return keys
