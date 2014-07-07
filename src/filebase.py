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

import os, sys

from lxml import etree

def parse_properties(fb):
	doc = fb["doc"]
	properties = []
	
	for p in doc.xpath("/filebase/properties/property"):
		properties.append({"id": int(p.attrib["id"]), "name": p.find("name").text})

	# Check if property id's are sequential
	for i in range(len(properties)):
		if properties[i]["id"] != i:
			sys.exit("ERROR: `property`s `id`s are not sequential")

	return properties

def parse_values(fb):
	doc = fb["doc"]
	properties = fb["properties"]
	values = []
	
	for pid in range(len(properties)):
		values.append([])

	for p in doc.xpath("//filebase/files/file/property"):
		if int(p.attrib["pid"]) > len(properties):
			sys.exit("ERROR: `pid` is wrong")

		if p.text not in values[int(p.attrib["pid"])]:
			values[int(p.attrib["pid"])].append(p.text)

	for pid in range(len(properties)):
		values[pid].sort()

	return values

def parse_filebase(path):
	fb = {}
	fb["doc"] = etree.parse(path)

	fb["properties"] = parse_properties(fb)
	fb["values"] = parse_values(fb)

	return fb

def build_XPath(fb, query_table):
	XPath = "/filebase/files/file["

	for pid in range(len(fb["properties"])):
		for i in range(len(fb["values"][pid])):
			if query_table[pid][i]:
				XPath += "property[@pid='{0}'] = '{1}' and ".format(pid, fb["values"][pid][i])

	if XPath ==  "/filebase/files/file[": # Nothing is selected, query all files
		XPath = XPath[:-1] # remove '[' at the end
	else:
		XPath = XPath[:-5] + "]" # remove 'and ' at the end and add ']' to end

	return XPath

def query_files(fb, query_table):
	doc = fb["doc"]
	files = []

	xpath = build_XPath(fb, query_table)	

	for f in doc.xpath(xpath):
		name = f.find("name").text
		path = f.find("path").text
		path.replace("/", os.sep)

		files.append({"name": name, "path": path})

	return files
