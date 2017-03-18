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

from werkzeug.wrappers import Request, Response
import traceback

from gethtml import getHtml
from zip import getZip

try:
    from sentry import Client
    client = Client()
except ImportError:
    client = None

@Request.application
def app(request):
    pres = request.args.get("p")
    if pres is None:
        pres = "welcome"
    
    get = request.args.get("get")
    if get is None:
        get = "html"
        
    url = request.url.replace("/index.py/?", "/?")

    try:
        if get == "zip":
            zipfile = getZip(pres, (get!="nojs"), url=url)
            Response(zipfile, mimetype="application/zip")
        else: # assume get == "html"
            html = getHtml(pres, (get!="nojs"), url=url)
            response = Response(html, mimetype="text/html")
    except:
        #raise
        #try:
        #    client.captureException()
        #    add_to_err = "This incident has been logged."
        #except AttributeError:
        #    add_to_err = "This incident hasn't been logged, because logging isn't configured."
        #except:
        #    add_to_err = "This incident hasn't been logged, because a error occured while logging the previous error."
        add_to_err = ""
        html = getHtml("error", (get!="nojs"), append={"text": add_to_err})
        response = Response(html, mimetype="text/html")
        traceback.print_exc()
    return (response)
