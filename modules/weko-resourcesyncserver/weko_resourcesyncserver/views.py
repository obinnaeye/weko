# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 National Institute of Informatics.
#
# WEKO-ResourceSyncServer is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module of weko-resourcesyncserver."""

# TODO: This is an example file. Remove it if you do not need it, including
# the templates and static folders as well as the test case.

from __future__ import absolute_import, print_function

from flask import Blueprint, render_template, jsonify
from flask_babelex import gettext as _

blueprint = Blueprint(
    'weko_resourcesyncserver',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.route("/")
def index():
    """Render a basic view."""
    return render_template(
        "weko_resourcesyncserver/index.html",
        module_name=_('WEKO-ResourceSyncServer'))


@blueprint.route("/resource_list")
def resource_list():
    """Render a basic view."""
    return jsonify(msg='resource list')


@blueprint.route("/resource_dump")
def resource_dump():
    """Render a basic view."""
    return jsonify(msg='resource dump')