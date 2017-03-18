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
import jinja2

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("."),
    autoescape=False
)

def getHtml(pres, js, prepend=False, append=False, url=""):
    folder = path.join("data", pres)
    with open(path.join(folder, "index.yaml")) as pres_file:
        pres_yaml = pres_file.read()
    pres_yaml = load(pres_yaml)
    markdown = Markdown(
        extensions=["extra", "codehilite", "wikilinks"],
        extension_configs={"codehilite": { "noclasses": True, "pygments_style": get_style_by_name(pres_yaml.get("pygments_style", "friendly")) }}
        )
    html = env.get_template("html.j2").render(
        js=js,
        title=pres_yaml.get("title", "Presentation"),
        subtitle=pres_yaml.get("subtitle", ""),
        author=pres_yaml.get("author", None),
        theme=pres_yaml.get("theme", "black"), # look at reveal.js/css/theme
        slides=pres_yaml,
        markdown=markdown,
        folder=folder,
        codecs=codecs,
        path=path,
        url=url,
        pres=pres,
        append=append,
        prepend=prepend,
        controls=pres_yaml.get("controls", "true"),
        progress=pres_yaml.get("progress", "true"),
        history=pres_yaml.get("history", "true"),
        center=pres_yaml.get("center", "true"),
        transition=pres_yaml.get("transition", "default") # default,cube,page,concave,zoom,linearfade,none
    )
    # remove empty lines:
    return "\n".join([line for line in html.split('\n') if line.strip()])

