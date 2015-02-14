#!/usr/bin/env pythona
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
# Author: Abelardo Pardo (abelardo.pardo@sydney.edu.au)
#

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

    if node["type"] == 'eqt':
        self.body.append('<img class="correct_icon"')
        self.body.append(' style="opacity: 0; margin-left: -23px;"')
        self.body.append(' src="%s"></img>' % os.path.join(node["p_to_static"],
                                                           'Correct_20x20.png'))
        self.body.append('<img class="incorrect_icon"')
        self.body.append(' style="opacity: 0; margin-left: -23px;"')
        self.body.append(' src="%s"></img>' 
                         % os.path.join(node["p_to_static"],
                                        'Incorrect_20x20.png'))
        self.body.append('<input type="radio" name="question" value="%s" />' % \
                         node["content"])
        return

    if node['type'] == 'eqt-fib':
        self.body.append('<div class="reauthoring_embedded_quiz-fib-answer">')
        self.body.append('Answer')
        self.body.append('<input type="text" name="question" value=""/></li>')
        self.body.append('<input type="hidden" name="solution" ')
        self.body.append('value="%s"/></li>' % node["content"])
        self.body.append('<img class="correct_icon" style="opacity: 0;')
        self.body.append('padding-left: 0.5em;"')
        self.body.append(' src="%s"></img>' % os.path.join(node["p_to_static"],
                                                           'Correct_20x20.png'))
        self.body.append('<img class="incorrect_icon" style="opacity: 0;"')
        self.body.append(' src="%s"></img>' 
                         % os.path.join(node["p_to_static"],
                                        'Incorrect_20x20.png'))
        self.body.append('</div>')
        return

    # If we reached this point in the function, there is a question type that is
    # new and has no corresponding code here!
    raise ValueError("Directive " + node['type'] + " has not been implemented")
    
def depart_eqt_answer_type_node(self, node):
    pass

class eqt(nodes.General, nodes.Element): pass

def visit_eqt_node(self, node):
    ### Need to check for the MODE!

    suffix = ''
    if node['name'] == 'eqt-fib':
        suffix = '-fib'
        
    self.body.append('<div class="reauthoring_embedded_quiz%s" id="%s">' 
                     % (suffix, node["args"][0]))
    self.body.append('<form class="reauthoring_embedded_quiz_questions">')

def depart_eqt_node(self, node):
    ### Need to check for the MODE!

    self.body.append('</form>')
    self.body.append('<div class="reauthoring_embedded_quiz_buttons">')
    self.body.append('<input class="reauthoring_quiz_button" style="display:none;" ')
    self.body.append('type="button" value="Grade" />')
    self.body.append('<input class="reauthoring_quiz_button" style="display:none;" ')
    self.body.append('type="button" value="Again" />')
    self.body.append('<input class="reauthoring_quiz_button" style="display:none;" ')
    self.body.append('type="button" value="Solution" />')
    self.body.append('</div>')
    self.body.append('</div>')

class Equestion(Directive):
    """
    Directive to insert a (single answer) multiple choice embedded question.
    The syntax is:

    .. eqt:: question-id

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

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()

        config = self.state.document.settings.env.config

        if config.config_values.get('eqt_question_type') != None:
            raise ValueError("Embedded questions cannot be nested.")

        # Store the type of question in an additional attribute in the
        # environment.
        config.config_values['eqt-question-type'] = self.name

        result = eqt(args = self.arguments, name = self.name)

        # Parse the nested content
        self.state.nested_parse(self.content, self.content_offset, result)

        # Remove the question type from the environment 
        del config.config_values['eqt-question-type']

        # If the question is a single MCQ, check that there is an enumerated
        # list and perform some additional tasks.
        if self.name == "eqt":
            # Loop over the question children to detect which one corresponds to
            # the list of answers and add some additional attributes
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
                answer_list_node['enumtype'] = answer_list_node['enumtype'] + \
                                               ' eqt-answer-list'
            else:
                raise ValueError('No anwer list found in e-question.')

        return [result]

def eqt_answer(name, rawtext, text, lineno, inliner,
                      options={}, content=[]):

    # print 'uuu', inliner.document.settings.env.config['AAA']

    # This role has only effect when in HTML mode.
    if inliner.document.settings.env.app.builder.format != 'html':
        return

    # Get the question type (if none, raise an exception).
    config = inliner.document.settings.env.config
    question_type = config.config_values.get('eqt-question-type')
    if question_type == None:
        raise ValueError('Role :eqt: must appear inside an embedded question.')

    # Single answer MCQ
    if question_type == 'eqt':
        # The value of the role can only be C or I (correct or incorrect)
        if text != 'C' and text != 'I':
            raise ValueError('Role text must be "C" or "I"')

    # Get the relative path to the static directory
    p_to_static = common.get_relative_path_to_static(inliner.document)

    return [eqt_answer_type(args = options,
                                   type = question_type,
                                   content = text,
                                   p_to_static = p_to_static)], []

class Equestion_fib(Directive):
    """
    Directive to insert a fill-in-the-blank quenestion.
    The syntax is:

    .. eqt-fib:: question-id
       :action: The url to send the result
       :id_field_name: field name in which to put the id
       :data_field_name: field name in which to put the data

       Text describing the question

       - :eqt:`C` Answer number 1 (which is correct)
       - :eqt:`I` Answer number 2 (which is incorrect)
       - :eqt:`I` Answer number 3 (which is incorrect)
       - :eqt:`I` Answer number 4 (which is incorrect)


    The three attributes of the directive (action, id_field_name, and
    data_field_name) can be set globally for an entire site in the conf.py file
    as:

    eqt_action = '<<YOUR ACTION>>'
    eqt_id_field_name = '<<FIELD NAME IN WHICH TO PUT IN THE ID>>'
    eqt_data_field_name = '<<FIELD NAME IN WHICH TO PUT THE DATA>>'
    pass
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
    app.add_directive("eqt-fib", Equestion)
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
