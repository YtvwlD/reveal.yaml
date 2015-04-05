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

from os import path
from werkzeug.serving import run_simple
from werkzeug.wsgi import SharedDataMiddleware

import main

app = SharedDataMiddleware(main.app,
	{
	"/reveal.js":	path.join(path.dirname(__file__), "reveal.js"),
	"/data":		path.join(path.dirname(__file__), "data")
	})
if __name__ == "__main__":
	run_simple("localhost", 4000, app)