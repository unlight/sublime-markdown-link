from urllib.request import urlopen, Request
from string import Template
import re

def get_file_contents(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
    }
    req = Request(url = url, headers = headers)
    try:
        return urlopen(req).read().decode('utf-8')
    except Exception as e:
        return None

markdown_link_template = Template('[$name]($link)')

def convert_markdown_link(link, content = None):
    result = link
    if content is None:
        content = get_file_contents(link)
    if content is not None and len(content) > 0:
        match = re.search(r'<h1[^>]*>(.+?)</h1>', content, re.DOTALL)
        if match is not None:
            name = match.group(1)
            if name is not None and len(name) > 0:
                name = name.replace('&nbsp;', ' ')
                name = re.sub(r'\s', ' ', name)
                name = re.sub(r'\s+', ' ', name)
                name = re.sub(r'\s+', ' ', name)
                name = name.strip()
                result = markdown_link_template.substitute(name = name, link = link)
    return result
