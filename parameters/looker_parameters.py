from abc import abstractmethod

class LookParams():
    def __init__(self, execution_timestamp, id, model, view, 
                fields = None, filters = None, 
                sorts = None, limit = None, 
                initial_load = False):
        self.execution_timestamp = execution_timestamp

        self.model = model
        self.view = view
        self.id = id

        self.initial_load = initial_load
        
        self.fields = fields
        self.filters = filters
        self.sorts = sorts
        self.limit = limit

    @abstractmethod
    def generate_id(self, id):
        if not id:
            return f"{self.model}::{self.view}"
        return id
    
    @abstractmethod
    def generate_fields(self, fields):
        if not fields:
            return []
        return fields

    @abstractmethod
    def generate_filters(self, filters):
        # https://cloud.google.com/looker/docs/filter-expressions
        if not filters:
            return {}
        return filters

    @abstractmethod
    def generate_sorts(self, sorts):
        # Use the format `["view.field", ...]` to sort on fields in ascending order. 
        # Use the format `["view.field desc", ...]` to sort on fields in descending order.
        # sorts = ['content_usage.other_count']
        if not sorts:
            return None
        return sorts

    @abstractmethod
    def generate_limits(self, limits):
        if not limits:
            return None
        return limits
    