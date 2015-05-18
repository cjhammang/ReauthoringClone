#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 The University of Sydney
# This file is part of the Reauthoring toolkit

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor
# Boston, MA  02110-1301, USA.
#
# Authors: Abelardo Pardo (abelardo.pardo@sydney.edu.au)
#          Xavier Ochoa (xavier@cti.espol.edu.ec)
#

from __future__ import division

import os, re, sys
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

from Sphinx_ext import html_form, common

class embedded_video(nodes.General, nodes.Element): pass

def visit_embedded_video_node(self, node):
    # Initialize variables for start and end of segment
    start="0"
    end="10000000" #Hopefully higher than any real value

    # Get the argument
    video_id = node["args"][0]
    # If only start is set
    if len(node["args"]) == 2:
        start = node["args"][1]
    # If start and end are set
    if len(node["args"]) == 3:
        start = node["args"][1]
        end = node["args"][2]


    # Get the params
    elem_id = node['element_id']
    height = node['height']
    width = node['width']

    # Deploy the div with the script inside
    self.body.append('<div id="%s" class="embedded-video">' % elem_id)
    self.body.append('<script type="text/javascript">')
    self.body.append("""array_video_embed['%s'] = {height: '%s',
                                        width: '%s',
                                        videoId: '%s',
                                        playerVars: {rel: 0, start: '%s', end: '%s'},
                                        events: {'onStateChange': onPlayerStateChange}};""" % \
                         (elem_id, height, width, video_id, start, end))
    self.body.append("</script>")
    self.body.append("</div>")


def depart_embedded_video_node(self, node):
    pass

class Embedded_video(Directive):
    """
    Directive to embed a youtube video, deploy the API and track events on the video.

    .. embedded-video:: videoId
       :height: value
       :width: value


    """

    has_content = False
    required_arguments = 1 # videoId
    optional_arguments = 2 # start end
    final_argument_whitespace = False
    option_spec = {
        "height": directives.nonnegative_int,
        "width": directives.nonnegative_int
        }

    def run(self):
        config = self.state.document.settings.env.config

        height = common.get_parameter_value(config, self.options, 'height',
                                            'embedded_video_height')
        width = common.get_parameter_value(config, self.options, 'width',
                                           'embedded_video_width')

        element_id = 'embedded-video-%s' % \
            self.state.document.settings.env.new_serialno('embedded-video')

        return [embedded_video(args = self.arguments,
                               element_id = element_id,
                               height = height,
                               width = width)]

def setup(app):
    app.add_node(embedded_video,
                 html = (visit_embedded_video_node,
                         depart_embedded_video_node))

    app.add_directive("embedded-video", Embedded_video)

    app.add_config_value('embedded_video_height', 390, True)
    app.add_config_value('embedded_video_width', "100%", True)
