# -*- encoding: utf-8 -*-
from collections import OrderedDict

import urwid
from urwid import Widget, WidgetWrap, Text, Columns, Frame, AttrMap, SimpleFocusListWalker, ListBox, Padding

from .palette import B16

class TableRow(Columns):

	def __init__(self, data, parent, color=None, **kwargs):
		self.table = parent

		self.color = color

		self.dict = data

		Columns.__init__(self, [], **kwargs)

		for header in self.table.columns:
			self.contents.append(self.build_cell(header))

	def __getitem__(self, key):
		return self.dict[key]

	def __setitem__(self, key, value):
		self.dict[key] = value

		# get index from table
		i = self.table.columns.keys().index(key)

		# rebuild the column cell
		column = self.build_cell(key)

		# this should _invalidate() the Columns
		self.contents[i] = column

	def build_cell(self, key):
		# get column options by key
		opt = self.table.columns[key]

		if 'gen' in opt:
			# generate value if column is dynamic
			column = opt['gen'](self.dict)
		else:
			column = self.dict[key]

		# only format non-widgets
		if 'format' in opt and not isinstance(column, Widget):
			# apply formatting function
			column = opt['format'](column)

		# default formatting
		if isinstance(column, (int, long, float, complex)):
			column = str(column)
		
		# wrap in Text() if column isn't a widget yet
		if not isinstance(column, Widget):
			column = Text(column)

		if 'color' in opt:
			fg, bg = opt['color']
			if self.color is not None:
				if fg is None:
					fg = self.color[0]
				if bg is None:
					bg = self.color[1]		
			column = AttrMap(column, B16(fg, bg))
		#elif self.color is not None:
		#	fg, bg = self.color
		#	column = AttrMap(column, B16(fg, bg))

		# add column size
		col_options = self.size_options(*opt['size']) if 'size' in opt else self.size_options()
		cwidget = (column, col_options)
		return cwidget

	@staticmethod
	def size_options(width_type='weight', width_amount=1, box_widget=False):
		if width_type == 'pack':
			width_amount = None
		if isinstance(width_type, int):
			width_amount = width_type
			width_type = 'given'
		if width_type not in ('pack', 'given', 'weight'):
			raise Exception('Tablerow: invalid column size')
		return (width_type, width_amount, box_widget)

class TableBox(WidgetWrap):

	headers = False

	dividechars = 0
	min_width = 1

	zebra = False
	odd = (None, 'darker gray')
	even = (None, None)

	row_factory = TableRow

	listbox = None

	def __init__(self, rows, columns, title=None, headers=False, zebra=False, dividechars=1, padding=None, row_factory=None):
		self.columns = columns
		self.headers = headers
		self.zebra = zebra
		self.dividechars = dividechars
		if row_factory is not None:
			self.row_factory = row_factory


		_rows = []

		if self.headers:
			header = Columns([],dividechars=self.dividechars, min_width=self.min_width)
			for k in columns:
				head = columns[k].get('header', k)
				size = TableRow.size_options(*columns[k]['size']) if 'size' in columns[k] else TableRow.size_options()
				header.contents.append( (Text(head), size) )
			header = AttrMap(header, 'table_header')

				
		for i, row in enumerate(rows):
			r = self.build_row(row, i)
			_rows.append(r)

		self.listwalker = SimpleFocusListWalker(_rows)
		self.listbox = ListBox(self.listwalker)
		self.frame = Frame(self.listbox)
		widget = self.frame
		if padding is not None:
			widget = Padding(self.frame, left=padding[0], right=padding[1])

		if self.headers:
			self.set_title(header)
		elif title:
			self.set_title(title)

		self.__super.__init__(widget)

	def set_title(self, txt):
		if not isinstance(txt, Widget):
			txt = Text(txt)
		self.frame.header = txt
		self.title = txt

	def build_row(self, data, i):
		tablerow = data
		if not isinstance(tablerow, Widget):
			color = None
			if self.zebra:
				color = self.even if (i+1) % 2 == 0 else self.odd
			tablerow = self.row_factory(tablerow, parent=self, color=color, dividechars=self.dividechars, min_width=self.min_width)

			if self.zebra:
				tablerow = AttrMap(tablerow, B16(*color))
		return tablerow

	def __getitem__(self, idx):
		if hasattr(self.listwalker[idx], 'original_widget'):
			return self.listwalker[idx].original_widget
		else:
			return self.listwalker[idx]

	def __setitem__(self, idx, value):
		self.listwalker[idx] = self.build_row(value, idx)

	def __delitem__(self, idx):
		del self.listwalker[idx]

	def __len__(self):
		return len(self.listwalker)

	def __iter__(self):
		return iter(self.listwalker)

	def insert(self, idx, value):
		self.listwalker.insert(idx, self.build_row(value, idx))

	def append(self, value):
		idx = len(self.listwalker)
		self.listwalker.append(self.build_row(value, idx))



#def rows(self, size, focus=False):
#	return len(self.listwalker)

class LabelBox(TableBox):
	def __init__(self, rows, kcol=dict(), vcol=dict(), **kwargs):
		_rows = []
		for k in rows:
			r = {'key': k, 'val': rows[k]}
			_rows.append(r)
		cols = OrderedDict([('key', kcol), ('val', vcol)])
		TableBox.__init__(self, _rows, cols, **kwargs)


## Column options
# header_label
#
# size -- (width_type, width_amount, box_widget)
# gen  -- dynamic column value generator
# format -- format function, applied when column value is not a widget
# color -- (foreground, background)
#
# align
# padding
# valign
# vpadding



