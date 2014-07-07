# coding: utf-8
import urwid



class FrameView(urwid.WidgetWrap):
	keymap = {}

	def __init__(self, app, frame):
		self.app = app
		self.frame = frame
		self.__super.__init__(self.frame)

	def footer_command(self, cmdline, callback):
		self.cmdline = cmdline
		self.frame.set_footer(cmdline)
		self.frame.set_focus('footer')
		urwid.connect_signal(cmdline, 'done', callback)

	def footer_clear(self, callback):
		urwid.disconnect_signal(self.cmdline, 'done', callback)
		self.frame.set_footer(None)
		self.cmdline = None
