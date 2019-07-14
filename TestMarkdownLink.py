import sublime
# import sys
from unittest import TestCase
# MarkdownLink = sys.modules['MarkdownLink.MarkdownLink']
# print("sys.modules", sys.modules)
# utils = sys.modules['ImportHelper.utils']

class TestMarkdownLink(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        # make sure we have a window to work with
        s = sublime.load_settings('Preferences.sublime-settings')
        s.set('close_windows_when_empty', False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command('close_file')

    def testSmoke(self):
        setText(self.view, '')
        self.assertEqual('', getAll(self.view))

    def testConvertLinkExample(self):
        setText(self.view, 'http://example.com/')
        self.view.run_command('select_all')
        self.view.run_command('markdown_link')
        self.assertEqual('[Example Domain](http://example.com/)', getAll(self.view))

    def testUnknownUrl(self):
        setText(self.view, 'unknown://example.com/')
        self.view.run_command('select_all')
        self.view.run_command('markdown_link')
        self.assertEqual('unknown://example.com/', getAll(self.view))

def setText(view, string):
    view.run_command('select_all')
    view.run_command('left_delete')
    view.run_command('insert', {'characters': string})

def getAll(view):
    return view.substr(sublime.Region(0, view.size()))

def getRow(view, row):
    return view.substr(view.line(view.text_point(row, 0)))
