#!/usr/bin/env python
from os import path
from werkzeug.serving import run_simple
from werkzeug.wsgi import SharedDataMiddleware
from index import app

middlewareApp = SharedDataMiddleware(app,
	{
	"/reveal.js":	path.join(path.dirname(__file__), "reveal.js"),
	"/data":		path.join(path.dirname(__file__), "data")
	})
if __name__ == "__main__":
	run_simple("localhost", 4000, middlewareApp)