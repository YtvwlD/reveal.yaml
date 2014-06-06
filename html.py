from os import path
from yaml import load
from markdown import Markdown

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
	html += parse_slide(pres_yaml, 2, markdown)
	#TODO: divs and ids
	html += "\t</body>\n"
	html += "</html>\n"
	return(html)

def parse_slide(slide, tabs, markdown):
	slide_html = ""
	tabs_to_insert = ""
	for i in xrange(tabs):
		tabs_to_insert += "\t"
	try:
		slide_html += tabs_to_insert + parse_md(slide["md"]) + "\n"
	except KeyError:
		try:
			slide_html += tabs_to_insert + slide["text"] + "\n"
		except KeyError:
			for x in slide["slides"]:
				slide_html += parse_slide(x, tabs + 1)

	return (slide_html)

def parse_md(md_file, markdown):
	return (markdown.reset().convertFile(path.join(folder, md)))
