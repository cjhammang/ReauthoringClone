#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import re, sys
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.misc import Class
from docutils.transforms import misc

from sphinx import addnodes
from sphinx.util.compat import Directive
from sphinx.util.nodes import set_source_info

class Instructor_guide(Directive):
    """
    Directive to insert content only for the instructor guide. The directive has
    two possible versions and relies on already existing nodes:

    .. iguide:: Instructor guide

    which is equivalent to:

    .. only:: iguide

       .. admonition:: Instructor guide
          :class: iguide

          TEXT GIVEN IN THE DIRECTIVE

    """

    has_content = True
    required_arguments = 1
    final_argument_whitespace = True

    def run(self):
        self.assert_has_content()

        node = addnodes.only()
        node.document = self.state.document
        set_source_info(self, node)
        node['expr'] = 'iguide'

        text = '\n'.join(self.content)
        admonition_node = nodes.admonition(text, **self.options)
        self.add_name(admonition_node)
            
        title_text = self.arguments[0]
        textnodes, messages = self.state.inline_text(title_text,
                                                     self.lineno)
        admonition_node += nodes.title(title_text, '', *textnodes)
        admonition_node += messages
        admonition_node['classes'] += ['iguide']
        
        self.state.nested_parse(self.content, self.content_offset,
                                admonition_node)
        node += admonition_node

        return [node]
            
class Instructor_guide_section(Directive):
    """
    Directive to insert content only for the instructor guide. The directive has
    two possible versions and relies on already existing nodes:

    .. iguide-section:: label

    which is equivalent to:

    .. only:: iguide
       
       .. rst-class:: iguide objectives

       TEXT GIVEN IN THE DIRECTIVE

    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        node = addnodes.only()
        node.document = self.state.document
        set_source_info(self, node)
        node['expr'] = 'iguide'

        class_value = ['iguide', self.arguments[0]]
            
        pending = nodes.pending(misc.ClassAttribute,
                                {'class': class_value, 
                                 'directive': self.name},
                                self.block_text)
        self.state_machine.document.note_pending(pending)
        node += pending

        self.state.nested_parse(self.content, self.content_offset, node,
                                match_titles=1)
        return [node]
            
def setup(app):
    app.add_directive("iguide", Instructor_guide)
    app.add_directive("iguide-section", Instructor_guide_section)

    
