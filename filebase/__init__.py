import os, sys

from lxml import etree

from . import filebase

def parse_filebase(path):
	if not os.path.isfile(path):
		sys.exit("File not exist: " + path)
	
	fb = {}
	fb["doc"] = etree.parse(path)

	fb["properties"] = filebase.parse_properties(fb)
	fb["values"] = filebase.parse_values(fb)

	return fb

def query_files(fb, query_table):
	doc = fb["doc"]
	files = []

	xpath = filebase.build_XPath(fb, query_table)	

	for f in doc.xpath(xpath):
		name = f.find("name").text
		path = f.find("path").text
		path.replace("/", os.sep)

		files.append({"name": name, "path": path})

	return files
