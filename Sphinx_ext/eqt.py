#!/usr/bin/env pythona
# -*- coding: utf-8 -*-

from __future__ import division

import os, sys
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import roles
from sphinx.util.compat import Directive
from docutils.utils import relative_path

from Sphinx_ext import html_form, common

class eqt_answer_type(nodes.General, nodes.Element): pass

def visit_eqt_answer_type_node(self, node):
    ### Need to check for the MODE!

    self.body.append('<img class="correct_icon"')
    self.body.append(' style="opacity: 0; margin-left: -23px;"')
    self.body.append(' src="%s"></img>' % os.path.join(node["p_to_static"],
                                                       'Correct_20x20.png'))
    self.body.append('<img class="incorrect_icon"')
    self.body.append(' style="opacity: 0; margin-left: -23px;"')
    self.body.append(' src="%s"></img>' %os.path.join(node["p_to_static"],
                                                      'Incorrect_20x20.png'))
    self.body.append('<input type="radio" name="question" value="%s" />' % \
                         node["type"])

def depart_eqt_answer_type_node(self, node):
    pass

class eqt(nodes.General, nodes.Element): pass

def visit_eqt_node(self, node):
    ### Need to check for the MODE!

    form_target = node["args"][0] + '_response'

    # Get the parameters
    method = node["method"]
    action = node["action"]

    self.body.append('<div class="adagio_embedded_quiz" id="%s">' % node["args"][0])
    self.body.append('<form method="%s" action="%s" target="%s">' % \
                         (method, action, form_target))
    self.body.append('<input type="hidden" name="%s"/>' % node["id_field_name"])
    self.body.append('<input type="hidden" name="%s"/>' % node["data_field_name"])
    self.body.append('</form>')
    self.body.append('<form class="adagio_embedded_quiz_questions">')

def depart_eqt_node(self, node):
    ### Need to check for the MODE!

    form_target = node["args"][0] + '_response'

    self.body.append('</form>')
    self.body.append('<div class="adagio_embedded_quiz_buttons">')
    self.body.append('<input class="adagio_quiz_button" style="display:none;" ')
    self.body.append('type="button" value="Grade" />')
    self.body.append('<input class="adagio_quiz_button" style="display:none;" ')
    self.body.append('type="button" value="Again" />')
    self.body.append('<input class="adagio_quiz_button" style="display:none;" ')
    self.body.append('type="button" value="Solutions" />')
    self.body.append('</div>')
    self.body.append('</div>')

class Equestion(Directive):
    """
    Directive to insert an embedded question feedback. The proposed structure is:

    .. eqt:: question-id
       :action: The url to send the result
       :id_field_name: field name to put the id
       :data_field_name: field name to put the data

       Text describing the question

       - :eqt:`C` Answer number 1 (which is correct)
       - :eqt:`I` Answer number 2 (which is incorrect)
       - :eqt:`I` Answer number 3 (which is incorrect)
       - :eqt:`I` Answer number 4 (which is incorrect)

    """

    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "action": directives.uri,
        "id-field-name": directives.unchanged,
        "text-field-name": directives.unchanged
        }

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()

        config = self.state.document.settings.env.config

        if 'action' not in self.options:
            action = config["eqt_action"]
            if action == None:
                raise ValueError('Config var eqt_action must be set')
        else:
            action = self.options["action"]

        if "id-field-name" not in self.options:
            id_field_name = config["eqt_id_field_name"]
            if id_field_name == None:
                raise ValueError('Unset config var eqt_id_field_name')
        else:
            id_field_name = self.options["id-field-name"]

        if "data-field-name" not in self.options:
            data_field_name = config["eqt_data_field_name"]
            if data_field_name == None:
                raise ValueError('Unset config var eqt_data_field_name')
        else:
            data_field_name = self.options["data-field-name"]

        method = self.options.get('method', None)
        if method == None:
            method = config["eqt_submit_method"]

        result = eqt(args = self.arguments,
                            action = action,
                            id_field_name = id_field_name,
                            data_field_name = data_field_name,
                            method = method)

        # Parse the nested content
        self.state.nested_parse(self.content, self.content_offset, result)

        # Loop over the question children to detect which one correspond to the
        # list of answers and add some additional attributes
        answer_list_node = None
        for question_child in result.children:
            if question_child.__class__.__name__ != 'enumerated_list':
                continue

            # Try ot obtain the eqt_answer_type. If it fails, we are
            # processing a regular node so we keep processing children
            name = question_child.children[0].children[0].children[0].__class__.__name__
            if name == 'eqt_answer_type':
                answer_list_node = question_child
                break

        if answer_list_node != None:
            answer_list_node['enumtype'] = answer_list_node['enumtype'] + ' eqt-answer-list'
        else:
            raise ValueError('No anwer list found in e-question.')

        return [result]

def eqt_answer(name, rawtext, text, lineno, inliner,
                      options={}, content=[]):

    # This role has only effect when in HTML mode.
    if inliner.document.settings.env.app.builder.format != 'html':
        return

    # The value of the role can only be C or I (correct or incorrect)
    if text != 'C' and text != 'I':
        raise ValueError('Role text must be "C" or "I"')

    # Get the relative path to the static directory
    p_to_static = common.get_relative_path_to_static(inliner.document)

    return [eqt_answer_type(args = options,
                                   type = text,
                                   p_to_static = p_to_static)], []

def setup(app):

    app.add_node(eqt,
                 html = (visit_eqt_node,
                         depart_eqt_node),
                 latex = (visit_eqt_node,
                          depart_eqt_node),
                 text = (visit_eqt_node,
                         depart_eqt_node),
                 man = (visit_eqt_node,
                        depart_eqt_node),
                 texinfo = (visit_eqt_node,
                            depart_eqt_node))

    app.add_directive("eqt", Equestion)
    app.add_config_value('eqt_action', None, True)
    app.add_config_value('eqt_id_field_name', None, True)
    app.add_config_value('eqt_data_field_name', None, True)
    app.add_config_value('eqt_submit_method', 'POST', True)

    roles.register_local_role('eqt', eqt_answer)

    app.add_node(eqt_answer_type,
                 html = (visit_eqt_answer_type_node,
                         depart_eqt_answer_type_node),
                 latex = (visit_eqt_answer_type_node,
                          depart_eqt_answer_type_node),
                 text = (visit_eqt_answer_type_node,
                         depart_eqt_answer_type_node),
                 man = (visit_eqt_answer_type_node,
                        depart_eqt_answer_type_node),
                 texinfor = (visit_eqt_answer_type_node,
                             depart_eqt_answer_type_node))
