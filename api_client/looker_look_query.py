import sys
sys.path.append('..')

import json
from typing import cast, Dict, List, Union
from looker_sdk import models, error

from api_client.looker_connection import Connection
from parameters.looker_parameters import LookParams

class LookQuery():
    def __init__(self, look_params: LookParams) -> None:
        self.look_params = look_params
        # self.look_params = self.get_look_params()
        self.sdk = self.generate_sdk()
        self.request = self.generate_query_request()

    def generate_sdk(self):
        import os
        print(f"Processing: Generating Connection for Look #{self.look_params.id}")
        print(f"Processing: Config File Location - {os.getcwd()}")
        connection = Connection()
        return connection.sdk

    """
    Look Parameters:
    WriteQuery(model='system__activity', view='content_usage', fields=['content_usage.content_title', 'content_usage.content_type', 'content_usage.days_since_last_accessed'], pivots=None, fill_fields=None, filters={}, filter_expression=None, sorts=['content_usage.content_title'], limit=None, column_limit='50', total=None, row_total=None, subtotals=None, vis_config=None, filter_config=None, visible_ui_sections=None, dynamic_fields=None, client_id=None, query_timezone=None, runtime=None)
    """
    def get_look_params(self):
        print(f"Processing: Generating Parameters for Look #{self.look_params.id}")
        """Returns the query associated with a given look id."""
        try:
            look = self.sdk.look(str(self.look_params.id))
        except error.SDKError as e:
            raise Exception(f"Processing: Look #{self.look_params.id} parameters not generated due to {e}")
        else:
            look_params = look.query
        return look_params

    """
    https://www.googlecloudcommunity.com/gc/Developing-Applications/Can-I-query-system-activity-explores-using-sdk-method/m-p/576926
    https://cloud.google.com/looker/docs/filter-expressions
    """
    def generate_query_request(self):
        print(f"Processing: Generating Query for Look #{self.look_params.id}")
        query_request = models.WriteQuery(
            model=self.look_params.model,
            view=self.look_params.view,
            fields=self.look_params.fields,
            # pivots=self.look_params.pivots,
            # fill_fields=self.look_params.fill_fields,
            filters=self.look_params.filters,
            sorts=self.look_params.sorts,
            limit=self.look_params.limit,
            # column_limit=self.look_params.column_limit,
            # total=self.look_params.total,
            # row_total=self.look_params.row_total,
            # subtotals=self.look_params.subtotals,
            # dynamic_fields=self.look_params.dynamic_fields,
            # query_timezone=self.look_params.query_timezone,
        )
        print(f"Processing: Look #{self.look_params.id} - {query_request}")
        return query_request

    """
    https://github.com/looker-open-source/sdk-codegen/blob/23b3dbfa1761d8b5d6abf6bbaf59318b91082393/examples/python/run_look_with_filters.py#L62
    """
    def execute(self):
        """Runs the specified query with the specified filters."""
        print(f"Processing: Extracting Data for Look #{self.look_params.id}")
        
        try:
            TJson = List[Dict[str, Union[str, int, float, bool, None]]]
            json_ = self.sdk.run_inline_query("json", self.request, cache=False)
            json_resp = cast(TJson, json.loads(json_))
            return json_resp
        except Exception as e:
            print(f"Processing: Failed to get look #{self.look_params.id} due to {e}")
        return json.loads("{}")
        