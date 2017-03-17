#!/usr/bin/env python

# reveal.yaml - YAML-based presentations with reveal.js
# Copyright (C) 2014-2015 Niklas Sombert
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

import os

from zipfile import ZipFile
from tempfile import mktemp
from sys import argv

from gethtml import getHtml

def getZip(pres, js, url=""):
	zipfilename = mktemp(".zip")
	zipfile = ZipFile(zipfilename, "w")
	for root, dirs, files in os.walk(os.path.join("data", pres)):
		base = os.path.join(".", *(os.path.split(root)[2:]))
		for filename in files:
			zipfile.write(os.path.join(root,filename), os.path.join(base, filename))
	for root, dirs, files in os.walk("reveal.js"):
		for filename in files:
			zipfile.write(os.path.join(root, filename))
	#TODO: Does this work?
	HTMLfileName = mktemp()
	with open(HTMLfileName, "w") as HTMLfile:
		HTMLtext = getHtml(pres, True, url=url)
		HTMLfile.write(HTMLtext.encode("utf-8"))
	zipfile.write(HTMLfileName, "index.html")
	zipfile.close()
	with open(zipfilename, "r") as zipfile:
		response = zipfile.read()
	os.unlink(zipfilename)
	os.unlink(HTMLfileName)
	return response

if __name__ == "__main__":
	from argparse import ArgumentParser
	argparse = ArgumentParser()
	argparse.add_argument("presentation", help="which presentation to parse")
	argparse.add_argument("--javascript", help="whether to use JavaScript", default=True, type=bool)
	argparse.add_argument("target", help="the zipfile to output")
	args = argparse.parse_args()
	zipfile = getZip(args.presentation, args.javascript, " - local (so no URL) - ")
	with open(args.target, "w") as newzipfile:
		newzipfile.write(zipfile)
