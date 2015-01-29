#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import re, sys, os
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

from Sphinx_ext import common

################################################################################
#
# HTML FORM
#
################################################################################
class html_form(nodes.General, nodes.Element): pass

def visit_html_form_node(self, node):
    # Get the arguments
    form_id = node["args"][0]
    
    self.body.append('<div class="adagio_form">')
    self.body.append('<form>')

def depart_html_form_node(self, node):
    
    # Get the parameters and the args
    p_to_static = node["p_to_static"]
    form_id = node["args"][0]

    # Subject and Verb values and activity id
    self.body.append('<input type="hidden" name="form_id" value="%s"/>' %
                     form_id)

    # Submit button
    self.body.append('<div><button class="adagio_submit">' + 
                     node["button_name"] + '</button></div>')
    self.body.append("</form>")
    self.body.append('<img class="submit_ok_icon" style="display: none;" src="%s"></img>' \
                         % os.path.join(node["p_to_static"], 
                                        'Correct_20x20.png'))
    self.body.append("</div>")
    return

class Html_form(Directive):
    """
    Directive to insert a form element. The expected format is:

    .. html-form:: id
       :button_name: name of the submit button

    The code is sensitve to the following global variables:
    - html_button_name: name of the submit button (def. Submit)
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "button_name": directives.unchanged
        }

    def run(self):
        config = self.state.document.settings.env.config

        # Submit button text
        button_name = \
            common.get_parameter_value(config, 
                                       self.options, 
                                       'button_name',
                                       "html_form_submit_button_name",
                                       False)

        # Get the path to the static directory containing the images
        p_to_static = common.get_relative_path_to_static(self.state.document)

        new_node = html_form(args = self.arguments, 
                             button_name = button_name,
                             p_to_static = p_to_static)

        # Parse the nested content
        self.state.nested_parse(self.content, self.content_offset,
                                new_node)

        return [new_node]

################################################################################
#
# HTML input field
#
################################################################################
class html_input(nodes.General, nodes.Element): pass

def visit_html_input_node(self, node):
    # Get the arguments
    name = node["args"][0]
    
    # Get the parameters
    el_type = node["el_type"]
    checked = node["checked"]
    maxlength = node["maxlength"]
    value = node["value"]

    self.body.append('<input type="%s" name="%s"' % (el_type, name))

    if checked != '':
        self.body.append(' checked="%s"' % checked)
    if maxlength != '':
        self.body.append(' maxlength="%s"' % maxlength)
    if value != '':
        self.body.append(' value="%s"' % value)
    self.body.append('/>')

def depart_html_input_node(self, node):
    pass

class Html_input(Directive):
    """
    Directive to insert an input form (expected to be inside an html form)

    .. html-input:: name
       :type: default 'text'
       :checked: if it is a radio button
       :maxlength: maxlength
       :value: text value

    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "type": directives.unchanged,
        "checked": directives.unchanged,
        "maxlength": directives.positive_int,
        "value": directives.unchanged
    }

    def run(self):
        if 'type' in self.options:
            el_type = self.options["type"]
        else:
            el_type = 'text'

        if 'checked' in self.options:
            checked = self.options["checked"]
        else:
            checked = ''

        if 'maxlength' in self.options:
            maxlength = str(self.options["maxlength"])
        else:
            maxlength = ''

        if 'value' in self.options:
            value = self.options["value"]
        else:
            value = ''

        return [html_input(args = self.arguments, 
                          el_type = el_type, 
                          checked = checked,
                          maxlength = maxlength,
                          value = value)]
                      

################################################################################
#
# HTML Textarea
#
################################################################################
class html_textarea(nodes.General, nodes.Element): pass

def visit_html_textarea_node(self, node):
    # Get the arguments
    textarea_id = node["args"][0]
    
    # Get the parameters
    rows = node["rows"]
    columns = node["columns"]
    text = node.get('text', '')
    other_params = node.get('other_params', '')

    self.body.append('<textarea name="%s" rows="%s" cols="%s" %s>' % \
                         (textarea_id, rows, columns, other_params))
    self.body.append(text)
    self.body.append('</textarea>')

def depart_html_textarea_node(self, node):
    pass

class Html_textarea(Directive):
    """
    Directive to insert a textarea element (expected to be inside an html form)

    .. html-textarea:: id
       :rows: number
       :columns: number
       :text: To include in the area
       :other_params: Additional styles

    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "rows": directives.positive_int,
        "columns" : directives.positive_int,
        "text": directives.unchanged,
        "other_params": directives.unchanged
    }

    def run(self):
        rows = self.options.get('rows', 25)
        columns = self.options.get('columns', 80)
        text = self.options.get('text', '')

        return [html_textarea(args = self.arguments, rows = rows, 
                              columns = columns, text = text, 
                              other_params = self.options.get('other_params', ''))]

################################################################################
#
# SETUP
#
################################################################################
def setup(app):
    # html_form
    app.add_node(html_form, 
                 html = (visit_html_form_node, 
                         depart_html_form_node))
    app.add_directive("html-form", Html_form)

    app.add_config_value('html_form_submit_button_name', 'Submit', True)

    # html_input
    app.add_node(html_input,
                 html = (visit_html_input_node,
                         depart_html_input_node))
    app.add_directive("html-input", Html_input)

    # html_textarea
    app.add_node(html_textarea, 
                 html = (visit_html_textarea_node, 
                         depart_html_textarea_node))
    app.add_directive("html-textarea", Html_textarea)