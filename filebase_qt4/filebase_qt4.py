# Copyright (C) 2014 Bora Mert Alper <boramalper@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, sys, pipes

from PyQt4 import QtGui

import filebase

class winProperties(QtGui.QWidget):
	def __init__(self, fb, app):
		self.fb = fb
		
		QtGui.QWidget.__init__(self)
		gb = QtGui.QGroupBox("")
		form = QtGui.QFormLayout()

		self.checkbox = []
		for pid in range(len(fb["properties"])):
			self.checkbox.append([])
			label = QtGui.QLabel("<b>{0}</b>".format(fb["properties"][pid]["name"]))
			form.addRow(label)

			for i in range(len(fb["values"][pid])):
				self.checkbox[pid].append(0)
				self.checkbox[pid][i] = QtGui.QCheckBox(fb["values"][pid][i])
				form.addRow(self.checkbox[pid][i])

		search_button = QtGui.QPushButton("Search")
		search_button.clicked.connect(app.quit)
				
		gb.setLayout(form)
		scroll = QtGui.QScrollArea()
		scroll.setWidget(gb)
		scroll.setWidgetResizable(True)
		layout = QtGui.QVBoxLayout(self)
		layout.addWidget(scroll)

		layout.addWidget(search_button)

	def getFiles(self):
		query_table = []
		
		for pid in range(len(self.fb["properties"])):
			query_table.append([])
			for i in range(len(self.fb["values"][pid])):
				query_table[pid].append(self.checkbox[pid][i].isChecked())

		return filebase.query_files(self.fb, query_table)

	def closeEvent(self, event):
		sys.exit()	

class winFiles(QtGui.QWidget):
	def __init__(self, fb, app, files):		
		QtGui.QWidget.__init__(self)
		gb = QtGui.QGroupBox("")
		form = QtGui.QFormLayout()

		for f in files:
			label = QtGui.QLabel("<b>{0}</b>".format(f["name"]))

			open_button = QtGui.QPushButton("Open")
			open_button.clicked.connect(self.gui_make_openFile(f["path"]))

			opendir_button = QtGui.QPushButton("Open Directory")
			opendir_button.clicked.connect(self.gui_make_openDir(f["path"]))

			form.addRow(label, open_button)

		gb.setLayout(form)
		scroll = QtGui.QScrollArea()
		scroll.setWidget(gb)
		scroll.setWidgetResizable(True)
		layout = QtGui.QVBoxLayout(self)
		layout.addWidget(scroll)

		back_button = QtGui.QPushButton("Back")
		back_button.clicked.connect(app.exit)
		layout.addWidget(back_button)
		
	def gui_make_openFile(self, path):
		def gui_openFile():
			return os.system("xdg-open " + pipes.quote(path))

		return gui_openFile

	def gui_make_openDir(self, path):
		def gui_openDir():
			return os.system("xdg-open " + pipes.quote(os.path.dirname(path)))

		return gui_openDir

	def closeEvent(self, event):
		sys.exit()
