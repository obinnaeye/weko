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

"""Query parser."""

import json

from flask import current_app, request
from invenio_records_rest.errors import InvalidQueryRESTError
from weko_index_tree.api import Indexes
from invenio_search import RecordsSearch


def get_items_by_index_tree(index_tree_id):
    """Get tree items."""
    records_search = RecordsSearch()
    records_search = records_search.with_preference_param().params(
        version=False)
    records_search._index[0] = current_app.config['SEARCH_UI_SEARCH_INDEX']
    search_instance = item_path_search_factory(search=records_search, index_id=index_tree_id)
    search_result = search_instance.execute()
    rd = search_result.to_dict()

    return rd.get('hits').get('hits')


def get_item_changes_by_index(index_tree_id):
    """Get tree items."""
    records_search = RecordsSearch()
    records_search = records_search.with_preference_param().params(
        version=False)
    records_search._index[0] = current_app.config['SEARCH_UI_SEARCH_INDEX']
    search_instance = item_changes_search_factory(search=records_search, index_id=index_tree_id)
    search_result = search_instance.execute()
    rd = search_result.to_dict()

    return rd.get('hits').get('hits')


def item_path_search_factory(search, index_id=None):
    """
    Parse query using Weko-Query-Parser.

    :param search: Elastic search DSL search instance.
    :param index_id: Index Identifier contains item's path
    :returns: Tuple with search instance and URL arguments.
    """
    def _get_index_search_query():
        query_q = {
            "from": "0",
            "size": "10000",
            "_source": {
                "excludes": [
                    "content",
                    "_item_metadata"
                ]
            },
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "path.tree": "@index"
                            }
                        },
                        {
                            "match": {
                                "relation_version_is_last": "true"
                            }
                        }
                    ]
                }
            },
            "post_filter": {
                "bool": {
                    "should": [
                        {
                            "bool": {
                                "must": [
                                    {
                                        "match": {
                                        "publish_status": "0"
                                        }
                                    },
                                    {
                                        "range": {
                                            "publish_date": {
                                                "lte": "now/d"
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ],
                    "must": [
                        {
                            "terms": {
                                "path": []
                            }
                        }
                    ]
                }
            }
        }

        q = index_id
        if q:
            post_filter = query_q['post_filter']

            if post_filter:
                list_path = Indexes.get_list_path_publish(index_id)
                post_filter['bool']['must'] = {
                    "terms": {
                        "path": list_path
                    }
                }
            # create search query
            if q:
                try:
                    fp = Indexes.get_self_path(q)
                    query_q = json.dumps(query_q).replace("@index", fp.path)
                    query_q = json.loads(query_q)
                except BaseException:
                    pass
            return query_q

    # create a index search query
    query_q = _get_index_search_query()
    try:
        # Aggregations.
        extr = search._extra.copy()
        search.update_from_dict(query_q)
        search._extra.update(extr)
    except SyntaxError:
        q = request.values.get('q', '') if index_id is None else index_id
        current_app.logger.debug(
            "Failed parsing query: {0}".format(q),
            exc_info=True)
        raise InvalidQueryRESTError()
    return search


def item_changes_search_factory(search, index_id=None):
    """
    Parse query using Weko-Query-Parser.

    :param search: Elastic search DSL search instance.
    :param index_id: Index Identifier contains item's path
    :returns: Tuple with search instance and URL arguments.
    """
    def _get_index_search_query():
        query_q = {
            "from": "0",
            "size": "10000",
            "_source": {
                "excludes": [
                "content",
                "_item_metadata"
                ]
            },
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "path.tree": "@index"
                            }
                        },
                        {
                            "bool": {
                                "must_not": {
                                    "exists": {
                                        "field": "path.tree"
                                    }
                                }
                            }
                        }
                    ]
                }
            },
            "sort": {
                "_updated": {
                "order": "asc"
                }
            },
            "post_filter": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "publish_date": {
                                    "lte": "now/d"
                                }
                            }
                        }
                    ],
                    "should": [
                        {
                            "terms": {
                                "path": []
                            }
                        }
                    ]
                }
            }
        }

        q = index_id
        if q:
            post_filter = query_q['post_filter']

            if post_filter:
                list_path = Indexes.get_list_path_publish(index_id)
                post_filter['bool']['should'] = {
                    "terms": {
                        "path": list_path
                    }
                }
            # create search query
            if q:
                try:
                    fp = Indexes.get_self_path(q)
                    query_q = json.dumps(query_q).replace("@index", fp.path)
                    query_q = json.loads(query_q)
                except BaseException:
                    pass
            return query_q

    # create a index search query
    query_q = _get_index_search_query()

    try:
        search.update_from_dict(query_q)
    except SyntaxError:
        current_app.logger.debug(
                "Failed parsing query: {0}".format(query_q),
                exc_info=True)
        raise InvalidQueryRESTError()

    return search
