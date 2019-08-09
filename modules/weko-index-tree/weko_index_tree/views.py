# -*- coding: utf-8 -*-
#
# This file is part of WEKO3.
# Copyright (C) 2017 National Institute of Informatics.
#
# WEKO3 is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# WEKO3 is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WEKO3; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.

"""Blueprint for weko-index-tree."""

import os

from flask import Blueprint, request, jsonify
from .api import Indexes

from .utils import get_ES_records_data_by_index
from .config import WEKO_INDEX_TREE_RSS_DEFAULT_INDEX_ID, \
    WEKO_INDEX_TREE_RSS_DEFAULT_PAGE, WEKO_INDEX_TREE_RSS_DEFAULT_COUNT, \
    WEKO_INDEX_TREE_RSS_DEFAULT_TERM, WEKO_INDEX_TREE_RSS_DEFAULT_LANG


# Left available to be used in the future

blueprint = Blueprint(
    'weko_index_tree',
    __name__,
    url_prefix='/indextree',
    template_folder='templates',
    static_folder='static',
)

blueprint_api = Blueprint(
    'weko_index_tree',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint_api.route('/rss.xml', methods=['GET'])
def get_rss_data():
    """Get rss data based on term.

    Returns:
        xml -- RSS data
    """
    data = request.args
    index_id = int(data.get('index_id') or WEKO_INDEX_TREE_RSS_DEFAULT_INDEX_ID)
    # page = int(data.get('page') or WEKO_INDEX_TREE_RSS_DEFAULT_PAGE)
    # count = int(data.get('count') or WEKO_INDEX_TREE_RSS_DEFAULT_COUNT)
    # term = int(data.get('term') or WEKO_INDEX_TREE_RSS_DEFAULT_TERM)
    # lang = data.get('lang') or WEKO_INDEX_TREE_RSS_DEFAULT_LANG
    

    recursive_tree_ids = Indexes.get_recursive_tree_ids(index_id)

    return jsonify(recursive_tree_ids)
