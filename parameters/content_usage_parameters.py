import sys
sys.path.append('..')

from parameters.looker_parameters import LookParams

DEFAULT_FIELDS = ['content_usage.content_id', 'content_usage.content_title', 'content_usage.content_type', 
                    'content_usage.days_since_last_access_tiers','content_usage.days_since_last_accessed',
                    'content_usage.id','content_usage.api_count','content_usage.embed_count','content_usage.embed_count',
                    'content_usage.public_count','content_usage.schedule_count','content_usage.other_count',
                    'content_usage.last_accessed_time']
DEFAULT_FILTERS = { "content_usage.last_accessed_time": "1 day ago" }

class ContentUsageParams(LookParams):
    def __init__(self, execution_timestamp, id = None, data_fields = None, 
                 data_filters = None, column_sorts = None, rows_limit = None, 
                 initial_load = False):
        self.execution_timestamp = execution_timestamp
        
        self.model = "system__activity"
        self.view = "content_usage"
        self.id = self.generate_id(id)

        self.initial_load = initial_load

        self.fields = self.generate_fields(data_fields)
        self.filters = self.generate_filters(data_filters)
        self.sorts = self.generate_sorts(column_sorts)
        self.limit = self.generate_limits(rows_limit)
    
        super().__init__(self.execution_timestamp, self.id, self.model, self.view, 
                         self.fields, self.filters, 
                         self.sorts, self.limit, self.initial_load)
    
    def generate_fields(self, fields):
        if not fields:
            return DEFAULT_FIELDS
        
        return fields
    
    def generate_filters(self, filters):
        if self.initial_load:
            return {}
        
        if not filters:
            return DEFAULT_FILTERS

        return filters