#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import os, re, sys
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

from Sphinx_ext import html_form, common

class embedded_video(nodes.General, nodes.Element): pass

def visit_embedded_video_node(self, node):
    # Get the argument
    video_id = node["args"][0]

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
                                        playerVars: {rel: 0},
                                        events: {'onStateChange': onPlayerStateChange}};""" % \
                         (elem_id, height, width, video_id))
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
    required_arguments = 1
    optional_arguments = 0
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
    