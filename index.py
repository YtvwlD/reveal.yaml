#!/usr/bin/env python

from wsgiref.handlers import CGIHandler
from werkzeug.wrappers import Request, Response

def run(environ, start_response):
	request = Request(environ)

	try:
		pres = request.args.get("p")
	except:
		pres = ""

	html = "Almost nothing here."

	response = Response(html, mimetype="text/html")
	return (response(environ, start_response))

if __name__ == "__main__":
	CGIHandler().run(run)
