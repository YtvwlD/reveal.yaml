#!/usr/bin/env python

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

from wsgiref.handlers import CGIHandler
from werkzeug.wrappers import Request, Response

from zipfile import ZipFile
from tempfile import mktemp
import os

from html import getHtml

try:
	from sentry import Client
	client = Client()
except ImportError:
	client = None

def run(environ, start_response):
	request = Request(environ)

	pres = request.args.get("p")
	if pres is None:
		pres = "welcome"
	
	get = request.args.get("get")
	if get is None:
		get = "html"
		
	url = request.url.replace("/index.py/?", "/?")

	try:
		if get == "zip":
			zipfilename = mktemp(".zip")
			zipfile = ZipFile(zipfilename, "w")
			for root, dirs, files in os.walk(os.path.join("data", pres)):
				base = os.path.join(".", *(os.path.split(root)[2:]))
				for filename in files:
					zipfile.write(os.path.join(root,filename), os.path.join(base, filename))
			for root, dirs, files in os.walk("reveal.js"):
				for filename in files:
					zipfile.write(os.path.join(root, filename)
			#TODO: Does this work?
			HTMLfileName = mktemp()
			with open(HTMLfileName, "w") as HTMLfile:
				HTMLtext = getHtml(pres, True, url=url)
				HTMLfile.write(HTMLtext.encode("utf-8"))
			zipfile.write(HTMLfileName, "index.html")
			zipfile.close()
			with open(zipfilename, "r") as zipfile:
				response = Response(zipfile.read(), mimetype="application/zip")
			os.unlink(zipfilename)
			os.unlink(HTMLfileName)
		else: # assume get == "html"
			html = getHtml(pres, (get!="nojs"), url=url)
			response = Response(html, mimetype="text/html")
	except:
		try:
			client.captureException()
			add_to_err = "This incident has been logged."
		except AttributeError:
			add_to_err = "This incident hasn't been logged, because logging isn't configured."
		except:
			add_to_err = "This incident hasn't been logged, because a error occured while logging the previous error."
		html = getHtml("error", (get!="nojs"), append={"text": add_to_err})
		response = Response(html, mimetype="text/html")
	return (response(environ, start_response))

if __name__ == "__main__":
	CGIHandler().run(run)
