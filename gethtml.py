# reveal.yaml - YAML-based presentations with reveal.js
# Copyright (C) 2014-2017 Niklas Sombert
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
from pygments.styles import get_style_by_name
import jinja2

env = jinja2.Environment(
	loader=jinja2.FileSystemLoader("."),
	autoescape=False
)

def getHtml(pres, js, prepend=False, append=False, url=""):
	folder = path.join("data", pres)
	with open(path.join(folder, "index.yaml")) as pres_file:
		pres_yaml = pres_file.read()
	pres_yaml = load(pres_yaml)
	markdown = Markdown(
		extensions=["extra", "codehilite", "wikilinks"],
		extension_configs={"codehilite": { "noclasses": True, "pygments_style": get_style_by_name(pres_yaml.get("pygments_style", "friendly")) }}
		)
	slides_html = ""
	if prepend:
		slides_html += parse_slide(prepend, 4, markdown, folder, first=True)
	slides_html += parse_slide({
			"slides": [
				{"text": "<h1>{}</h1><br><h3>{}</h3>".format(pres_yaml.get("title", "Presentation"), pres_yaml.get("subtitle", ""))},
				{"text": "<h1>Online</h1><br><pre>{}</pre><br><a href='./?p={}&get=zip'>Download</a>".format(url, pres)}
				]
		}, 4, markdown, folder, first=True)
	slides_html += parse_slide(pres_yaml, 4, markdown, folder, first=True)
	if append:
		slides_html += parse_slide(append, 4, markdown, folder, first=True)
	return env.get_template("html.j2").render(
		js=js,
		title=pres_yaml.get("title", "Presentation"),
		subtitle=pres_yaml.get("subtitle", None),
		author=pres_yaml.get("author", None),
		theme=pres_yaml.get("theme", "black"), # look at reveal.js/css/theme
		slides_html=slides_html, # TODO
		controls=pres_yaml.get("controls", "true"),
		progress=pres_yaml.get("progress", "true"),
		history=pres_yaml.get("history", "true"),
		center=pres_yaml.get("center", "true"),
		transition=pres_yaml.get("transition", "default") # default,cube,page,concave,zoom,linearfade,none
	)

def parse_slide(slide, tabs, markdown, folder, first=False):
	slide_html = ""
	if not first:
		slide_html += "\t" * tabs + "<section>\n"
		tabs += 1
	if "md" in slide.keys():
		slide_html += "\t" * tabs + parse_md(slide["md"], tabs, markdown, folder) + "\n"
	elif "text" in slide.keys():
		slide_html += "\t" * tabs + slide["text"] + "\n"
	elif "slides" in slide.keys():
		for x in slide["slides"]:
			slide_html += parse_slide(x, tabs, markdown, folder)
	else:
		pass # If a slide is empty, don't put anything in it.
	if not first:
		tabs -= 1
		slide_html += "\t" * tabs + "</section>\n"
	return (slide_html)

def parse_md(md_file, tabs, markdown, folder):
	markdown.reset()
	with codecs.open(path.join(folder, md_file), encoding="UTF-8") as md:
		md_result = markdown.convert(md.read())
	md_result_with_tabs = ""
	code = False
	for line in md_result.splitlines():
		if line.startswith("<div class=\"codehilite\"><pre>"):
			code = True
		if not code:
			md_result_with_tabs += "\t" * tabs
		md_result_with_tabs += line + "\n"
		if line.endswith("</pre></div>"):
			code = False
	return (md_result_with_tabs)


