from urllib.request import urlopen
from string import Template
import re

def get_file_contents(url):
    try:
        return urlopen(url).read().decode('utf-8')
    except Exception as e:
        return None

markdown_link_template = Template('[$name]($link)')

def convert_markdown_link(link, content = None):
    result = link
    if content is None:
        content = get_file_contents(link)
    if content is not None and len(content) > 0:
        match = re.search(r'<h1[^>]*>(.+?)</h1>', content)
        if match is not None:
            name = match.group(1)
            if name is not None and len(name) > 0:
                result = markdown_link_template.substitute(name = name, link = link)
    return result
