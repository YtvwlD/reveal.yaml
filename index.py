#!/usr/bin/env python

from wsgiref.handlers import CGIHandler
from werkzeug.wrappers import Request, Response
from html import getHtml

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
			html = getHtml("error", True)
		response = Response(html, mimetype="text/html")
	return (response(environ, start_response))

if __name__ == "__main__":
	CGIHandler().run(run)
