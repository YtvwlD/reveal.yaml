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
from html import getHtml

try:
    from sentry import Client
    client = Client()
except:
    client = None

def run(environ, start_response):
	request = Request(environ)

	try:
		pres = request.args.get("p")
	except:
		pres = ""
	
	try:
		get = request.args.get("get")
	except:
		get = "html"

	if get == "nojs":
		try:
			html = getHtml(pres, False)
		except:
			html = getHtml("error", False)
		response = Response(html, mimetype="text/html")
	elif get == "zip":
		response = Response("", mimetype="application/zip")
	else: #assume get == "html"
		try:
			html = getHtml(pres, True)
		except:
			try:
				client.captureException()
			except:
				pass
			html = getHtml("error", True)
		response = Response(html, mimetype="text/html")
	return (response(environ, start_response))

if __name__ == "__main__":
	CGIHandler().run(run)
