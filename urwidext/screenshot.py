# coding: utf-8
import urwid


DEFAULT_TEMPLATE = '<html><head><meta charset="utf-8"></head><body><center>{0}</center></body>'


def take_screenshot(self, loop, filename=None, screen_dir=None, palette=list(), screen_size=(100,40), tpl=DEFAULT_TEMPLATE):
	if filename is not None:
		filename = '{0}.html'.format(filename)
	else:
		filename = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y_%H.%M.html')

	html = urwid.html_fragment.HtmlGenerator()
	html.register_palette(palette)
	#html.register_palette_entry(None, 'light gray', 'black')
	canvas = loop._topmost_widget.render(screen_size, focus=True)
	html.draw_screen(screen_size, canvas)

	filepath = '{0}/{1}'.format(screen_dir, filename)
	with open(filepath, 'wb') as f:
		f.write(tpl.format(html.fragments[-1]))
