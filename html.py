# reveal.yaml - YAML-based presentations with reveal.js
# Copyright (C) 2014 Niklas Sombert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from os import path
from yaml import load
from markdown import Markdown
import codecs

def getHtml(pres, js):
	folder = path.join("data", pres)
	with open(path.join(folder, "index.yaml")) as pres_file:
		pres_yaml = pres_file.read()
	pres_yaml = load(pres_yaml)

	markdown = Markdown(extensions=["extra", "codehilite", "wikilinks"])

	#much to do; now only parsing the slides and outputting pure html

	html = ""
	html += "<!doctype html>\n<html>\n"
	#TODO: HEAD
	html += "\t<body>\n"
	#TODO: divs and ids
	html += "\t\t<div class=\"reveal\">\n"
	html += "\t\t\t<div class=\"slides\">\n"
	html += parse_slide(pres_yaml, 4, markdown, folder)
	#TODO: divs and ids
	html += "\t\t\t</div>\n"
	html += "\t\t</div>\n"
	html += "\t</body>\n"
	html += "</html>\n"
	return(html)

def parse_slide(slide, tabs, markdown, folder):
	slide_html = ""
	tabs_to_insert = "\t" * tabs
	try:
		slide_html += tabs_to_insert + parse_md(slide["md"], markdown, folder) + "\n"
	except KeyError:
		try:
			slide_html += tabs_to_insert + slide["text"] + "\n"
		except KeyError:
			for x in slide["slides"]:
				slide_html += parse_slide(x, tabs + 1, markdown, folder)

	return (slide_html)

def parse_md(md_file, markdown, folder):
	markdown.reset()
	with codecs.open(path.join(folder, md_file), encoding="UTF-8") as md:
		md_result = markdown.convert(md.read())
	return (md_result)
