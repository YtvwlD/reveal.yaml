#!/usr/bin/env python

from wsgiref.handlers import CGIHandler
from main import app

if __name__ == "__main__":
	CGIHandler().run(app)