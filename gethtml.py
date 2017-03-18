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

def getHtml(pres, js, prepend=False, append=False, url=""):
	folder = path.join("data", pres)
	with open(path.join(folder, "index.yaml")) as pres_file:
		pres_yaml = pres_file.read()
	pres_yaml = load(pres_yaml)
	markdown = Markdown(
		extensions=["extra", "codehilite", "wikilinks"],
		extension_configs={"codehilite": { "noclasses": True, "pygments_style": get_style_by_name("friendly") }}
		)
	html = ""
	html += """
<!doctype html>
<html>
	<head>
		<meta charset="utf-8">

		<title>{0} - {1}</title>

		<meta name="description" content="{1}">
		<!--<meta name="author" content="Hakim El Hattab">-->

		<meta name="apple-mobile-web-app-capable" content="yes" />
		<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
""".format(pres_yaml.get("title", "presentation"), pres_yaml.get("subtitle", ""))
	if js:
		html += """
		<link rel="stylesheet" href="reveal.js/css/reveal.css">
		<link rel="stylesheet" href="reveal.js/css/theme/{}.css" id="theme">

		<!-- For syntax highlighting: TODO -->

		<!-- If the query includes 'print-pdf', include the PDF print sheet -->
		<script>
			if( window.location.search.match( /print-pdf/gi ) ) {{
				var link = document.createElement( 'link' );
				link.rel = 'stylesheet';
				link.type = 'text/css';
				link.href = 'reveal.js/css/print/pdf.css';
				document.getElementsByTagName( 'head' )[0].appendChild( link );
			}}
		</script>

		<!--[if lt IE 9]>
		<script src="reveal.js/lib/js/html5shiv.js"></script>
		<![endif]-->
		
		<script src="reveal.js/lib/js/head.min.js"></script>
		<script src="reveal.js/js/reveal.js"></script>
""".format(pres_yaml.get("theme", "default"))
	html += """
	</head>
	
	<body>
		<div class="reveal">
			<div class="slides">
"""
	if prepend:
		html += parse_slide(prepend, 4, markdown, folder, first=True)
	html += parse_slide({
			"slides": [
				{"text": "<h1>{}</h1><br><h3>{}</h3>".format(pres_yaml.get("title", "Presentation"), pres_yaml.get("subtitle", ""))},
				{"text": "<h1>Online</h1><br><pre>{}</pre><br><a href='./?p={}&get=zip'>Download</a>".format(url, pres)}
				]
		}, 4, markdown, folder, first=True)
	html += parse_slide(pres_yaml, 4, markdown, folder, first=True)
	if append:
		html += parse_slide(append, 4, markdown, folder, first=True)
	html += """
			</div>
		</div>
"""
	config = []
	dest_src_key_othwerwise(config, pres_yaml, "controls", "true")
	dest_src_key_othwerwise(config, pres_yaml, "progress", "true")
	dest_src_key_othwerwise(config, pres_yaml, "history", "true")
	dest_src_key_othwerwise(config, pres_yaml, "center", "true")
	dest_src_key_othwerwise(config, pres_yaml, "theme", "")
	dest_src_key_othwerwise(config, pres_yaml, "transition", "")
	if js:
		html += """
		<!-- TODO: Pull the configuration below from the YAML. -->
		<script>
			// Full list of configuration options available here:
			// https://github.com/hakimel/reveal.js#configuration
			Reveal.initialize({{
				controls: {},
				progress: {},
				history: {},
				center: {},
				theme: "{}" || Reveal.getQueryHash().theme || "default", // available themes are in /css/theme
				transition: "{}" || Reveal.getQueryHash().transition || "default", // default/cube/page/concave/zoom/linear/fade/none
				// Parallax scrolling
				// parallaxBackgroundImage: 'https://s3.amazonaws.com/hakim-static/reveal-js/reveal-parallax-1.jpg',
				// parallaxBackgroundSize: '2100px 900px',

				// Optional libraries used to extend on reveal.js
				dependencies: [
					{{ src: 'reveal.js/lib/js/classList.js', condition: function() {{ return !document.body.classList; }} }},
					{{ src: 'reveal.js/plugin/zoom-js/zoom.js', async: true, condition: function() {{ return !!document.body.classList; }} }},
					{{ src: 'reveal.js/plugin/notes/notes.js', async: true, condition: function() {{ return !!document.body.classList; }} }}
				]
			}});
		</script>
""".format(*config)
	html += """
	</body>
</html>
"""
	return(html)

def dest_src_key_othwerwise(dest, src, key, otherwise):
	try:
		dest.append(src[key])
	except KeyError:
		dest.append(otherwise)

def parse_slide(slide, tabs, markdown, folder, first=False):
	slide_html = ""
	if not first:
		slide_html += "\t" * tabs + "<section>\n"
		tabs += 1
	try:
		slide_html += "\t" * tabs + parse_md(slide["md"], tabs, markdown, folder) + "\n"
	except KeyError:
		try:
			slide_html += "\t" * tabs + slide["text"] + "\n"
		except KeyError:
			for x in slide["slides"]:
				slide_html += parse_slide(x, tabs, markdown, folder)
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


