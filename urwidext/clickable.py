# -*- coding: utf-8 -*-
import os
import sys
import contextlib
import webbrowser

from urwid import Text


class ClickableText(Text):
	def __init__(self, text, callback, **kwargs):
		self.click = callback
		Text.__init__(self, text, **kwargs)

	def mouse_event(self, size, event, button, col, row, focus):
		if button == 1:
			self.click()

class URLText(ClickableText):
	def __init__(self, text, url, **kwargs):
		self.url = url
		ClickableText.__init__(self, text, self.open_url, **kwargs)

	def open_url(self):
		with stdchannel_redirected(sys.stderr, os.devnull):
			webbrowser.open(self.url, 2)	

@contextlib.contextmanager
def stdchannel_redirected(stdchannel, dest_filename):
    """
    A context manager to temporarily redirect stdout or stderr

    e.g.:

    with stdchannel_redirected(sys.stderr, os.devnull):
        ...
    """

    try:
        oldstdchannel = os.dup(stdchannel.fileno())
        dest_file = open(dest_filename, 'w')
        os.dup2(dest_file.fileno(), stdchannel.fileno())

        yield
    finally:
        if oldstdchannel is not None:
            os.dup2(oldstdchannel, stdchannel.fileno())
        if dest_file is not None:
            dest_file.close()






