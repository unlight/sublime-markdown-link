from urllib.request import urlopen, Request
from string import Template
import re
from urllib.error import URLError
from bs4 import BeautifulSoup

markdown_link_template = Template("[$title]($link)")


def convert_markdown_link(link, content=None):
    result = link
    if content is None:
        content = get_file_contents(link)
    if content is not None and len(content) > 0:
        title = find_content_title(content)
        if title is not None and len(title) > 0:
            title = normalize_string(title)
            result = markdown_link_template.substitute(title=title, link=link)
    return result


def find_content_title(content):
    soup = BeautifulSoup(content, "html.parser")
    candidate_elements = [[], [], []]
    elements = soup.select('[itemprop="name"], h1')
    for element in elements:
        if element.attrs.get("itemprop") == "name":
            candidate_elements[0].append(element)
            break
        elif element.name == "h1":
            class_name = normalize_class_name(element.attrs.get("class"))
            for name in ["post-title", "entry-title", "page-title"]:
                if name in class_name:
                    candidate_elements[1].append(element)
            candidate_elements[2].append(element)
    candidate_elements = [
        element for sublist in candidate_elements for element in sublist
    ]
    if len(candidate_elements) == 0:
        return None
    element = candidate_elements[0]
    return element.get_text()


def normalize_class_name(name):
    t = type(name)
    if t is str:
        return name
    if t is list:
        return " ".join(name)
    return ""


def normalize_string(s):
    s = s.replace("&nbsp;", " ")
    s = re.sub(r"\s", " ", s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip()
    return s


def get_file_contents(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
    }
    try:
        req = Request(url=url, headers=headers)
        return urlopen(req).read().decode("utf-8")
    except Exception as err:
        print("MarkdownLink Request Error " + url + " " + str(err))
    return None


def clean_link(s):
    s = s.strip()
    return s
