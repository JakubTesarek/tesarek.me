import glob
import re
import subprocess
from os.path import dirname

HOST = 'https://tesarek.me/'
EXCLUDE = ['error-pages']

def get_files():
    files = glob.glob('**/*.md', recursive=True)
    return [f for f in files if dirname(f) not in EXCLUDE]


def get_url(file):
    return HOST + re.sub(r'/?(index)?\.md', '', file)


def get_lastmod_time(file):
    result = subprocess.run(
        ['git', 'log', '-1', '--format="%ad"', '--date=iso8601-strict', '--', file],
        stdout=subprocess.PIPE
    )
    return result.stdout.decode('utf-8').strip().replace('"', '')


def create_xml_url(loc, lastmod, changefreq='weekly', priority=1.0):
    return f'''
        <url>
            <loc>{loc}</loc>
            <lastmod>{lastmod}</lastmod>
            <changefreq>{changefreq}</changefreq>
            <priority>{priority}</priority>
        </url>
    '''


xml = ''
for file in get_files():
    xml += create_xml_url(get_url(file), get_lastmod_time(file))

xml = f'''
    <?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        {xml}
    </urlset>
'''
print(xml)
