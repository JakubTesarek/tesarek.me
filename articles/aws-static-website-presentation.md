# Static Websites in AWS

**Use only US-East (N. Virginia). Some functions are not available elsewhere.**

## Goal

- create static website using AWS technology
- no VPS
- accessible on www and non-www domains
- nice urls (*no .html*)
- https only
- publish content by pushing to git repo
- write content in markdown
- CDN

## S3
- 2 buckets for www and non-www version
- set public access to buckets
- set bucket policy on main bucket to make documents public
- enable static website hosting on main bucket
- enable requests redirects from secondary bucket
- you can sync local/\*.md with S3 using AWS-CLI: `aws s3 sync local s3://bucket.name --exclude "*" --include "*.md"`

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::bucket.name/*.html"
        }
    ]
}
```


## Route 53
- create new hosted zone for your domains
- switch NS servers to AWS
- setup MX records if necessery
- setup A record alias to CloudFront distribution (when ready)

## ACM
- request new certificate for your domain
- confirm your ownership of the domain

## CloudFront
- create new CloudFront distribution
- setup redirect from http to https
- use ACM provided certificate
- set origin to your main S3 bucket
- for debugging purpose disable caching
- go back to Route 53 and set A record alias to the CloudFront distribution

## Lambda
- create new Lambda@Edge
- use CloudFront trigger
- insert url rewrite rules

```
'use strict';
exports.handler = (event, context, callback) => {
    var request = event.Records[0].cf.request;
    var uri = request.uri;

    // Add /index.html to directory listings
    uri = uri.replace(/\/$/, '\/index.html');

    // Add .html when suffix missing
    uri = uri.replace(/\/([a-z0-9_\-]+)$/i, '/$1.html')

    console.log("Old URI: " + request.uri);
    console.log("New URI: " + uri);
    request.uri = uri;
    return callback(null, request);

};
```

## CircleCI

- add CircleCI integration to your Github
- in AWS IAM create new user with write access to S3
- in `workflow > build settings > environment variables` fill in following variables
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_DEFAULT_REGION`
- create directory `.circleci`
- create file `.circleci/requirements.txt` with content `awscli`
- create file `.circleci/config.yml` with content:

```
version: 2
jobs:
  build:
    docker:
      - image: circleci/python:3.6.1
    working_directory: ~/repo

    steps:
      - checkout

      - restore_cache:
          keys:
          - v1-dependencies-{{ checksum ".circleci/requirements.txt" }}
          - v1-dependencies-

      - run:
          name: install dependencies
          command: |
            python3 -m venv venv
            . venv/bin/activate
            pip install -r .circleci/requirements.txt

      - save_cache:
          paths:
            - ./venv
          key: v1-dependencies-{{ checksum ".circleci/requirements.txt" }}

      - run:
          name: sync with s3
          command: |
            . venv/bin/activate
            aws s3 sync . s3://bucket.name --exclude "*" --include "*.md"
```

## Pricing
All prices are per month

### S3
- 2,000 put requests in free tier / then $0.005 per 1,000 requests
- 20,000 get requests in free tier / then $0.0004 per 1,000 requests
- 5GB of storage in free tier / then $0.023 per GB
- deletes are free

### Cloudfront
- 2,000,000 requests in free tier / then ~$0.0100 per 10,000 requests
- 50GB out in free tier / then ~$0.080 per 1GB

### Lambda
- free tier doesn't expire
- 1,000,000 executions is free / then $0.20 per 1,000,000 executions
- 400,000 GB-seconds is free / then $0.00001667 per GB-second

### Route 53
- $0.50 per hosted zone
- $0.400 per 1,000,000 DNS requests

### CircleCI
- free for one project

### Github
- free for public projects

### Pricing example
**Average sized blog**

- 200 pages
- 250kB/page
- 10,000 pageviews/month (50% USA, 50% Europe)
- 500 page updates/month
- no caching

**Montly TCO**

- S3: $0.05
- Route 53: $0.50
- CloudFront: $0.28
- Lambda: fits in free tier
- **Total: $0,83/month**


## Bonus
You can automate S3 to generate html from md files.

- create new Lambda function
- use S3 trigger
- limit trigger to .md files only
- create new IAM role with read/write access to S3
- insert compiler code

```
import urllib.parse
import boto3
import re
import markdown2


s3 = boto3.client('s3')

def get_header(metadata):
    return f'''
<html>
    <header>
        <title>{metadata['title']}</title>
    </header>
<body style="font-size: 130%">
    '''


def get_footer():
    return '''
    </body>
</html>
    '''


def get_title(key):
    title = re.sub('^.*/', '', key)
    title = re.sub('\.\w+$', '', key)
    return title.replace('-', ' ')


def get_html_key(key):
    return re.sub('\.md$', '.html', key)


def write_html(bucket, key, content):
    content = content.encode("utf-8")
    bucket_name = bucket
    s3.put_object(Bucket=bucket, Key=key, Body=content, ContentType='text/html')


def get_html(key, md_body):
    html_body = markdown2.markdown(md_body, extras=[
            'fenced-code-blocks',
            'header-ids',
            'metadata'
        ])
    metadata = html_body.metadata
    metadata.setdefault('title', get_title(key))
    return get_header(html_body.metadata) + html_body + get_footer()


def get_md(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    return response['Body'].read().decode('utf-8')


def parse_event(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8'
    )
    return bucket, key


def lambda_handler(event, context):
    try:
        bucket, key = parse_event(event)
        md_body = get_md(bucket, key)
        html_key = get_html_key(key)
        html_body = get_html(key, md_body)
        write_html(bucket, html_key, html_body)
        return True
    except Exception as e:
        print(e)
        raise e
```

*The above code is dependent on [Markdown2](https://github.com/trentm/python-markdown2). You can just insert the code, no need for instalation*
