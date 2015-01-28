#!/usr/bin/env pythona
# -*- coding: utf-8 -*-

import sys,os

def get_relative_path_to_static(document):
    docname = document.get("source")
    srcdir = document.settings.env.srcdir
    # build_suffix = os.path.dirname(docname).replace(srcdir, '')
    build_suffix = os.path.dirname(docname)[len(srcdir):]
    if build_suffix != '':
        build_suffix = build_suffix[1:]

    builder = document.settings.env.app.builder
    build_dir = os.path.join(builder.outdir, build_suffix)
    static_dir = os.path.join(builder.outdir, '_static')

    return os.path.relpath(static_dir, build_dir)

def get_parameter_value(config, options, key, config_key, enforce_set = True):
    value = options.get(key, None)
    if value == None:
        value = config[config_key]
        if enforce_set and value == None:
            raise ValueError('Unset config var ' + config_key)
    return value

def get_enclosing_activity_id(node):
    """
    Function that traverses the tree upwards through the parent relationship
    until a node is detected with the "activity" and "section" classes. When
    found, it returns the IDs attribute. None if not found.
    """
    start = node;
    while ((not "activity" in start.attributes['classes'] or \
                start.tagname != "section") and \
               start.parent != None):
        start = start.parent

    if "activity" in start.attributes['classes'] and \
            start.tagname == "section":
        return start.attributes['ids'][0]

    return None

