import sublime
import sys
from unittest import TestCase
# import_helper = sys.modules['ImportHelper.import_helper']
# utils = sys.modules['ImportHelper.utils']

class TestMarkdownLink(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def test_smoke(self):
        setText(self.view, '')
        self.assertEqual('', getAll(self.view))

def setText(view, string):
    view.run_command("select_all")
    view.run_command("left_delete")
    view.run_command("insert", {"characters": string})

def getAll(view):
    return view.substr(sublime.Region(0, view.size()));

def getRow(view, row):
    return view.substr(view.line(view.text_point(row, 0)))
