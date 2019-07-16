import sublime
import sublime_plugin
import os
import sys
# stupid python module system
package_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(package_directory)
from bs4 import BeautifulSoup
sys.path.remove(package_directory)
from .Utils import convert_markdown_link

# view.run_command('markdown_link', args=({}))
# http://example.com
# foo://example.com

class MarkdownLinkCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for selection in self.view.sel():
            if selection.empty():
                continue
            link = self.view.substr(selection)
            markdown_link = convert_markdown_link(link)
            if link != markdown_link:
                self.view.replace(edit, selection, markdown_link)
