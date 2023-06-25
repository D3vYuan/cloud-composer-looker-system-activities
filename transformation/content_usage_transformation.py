from json_converter.json_mapper import JsonMapper
import json
import re

class ContentUsageTransformation():
    def __init__(self, raw_message):
        self.raw_message = self.pre_processed(raw_message)
        self.specification = {
            '$on': 'result',
            'content_id': ["content_id"],
            'content_title': ["content_title"],
            'content_type': ["content_type"],
            'days_since_last_access_tiers': ["days_since_last_access_tiers"],
            'days_since_last_accessed': ["days_since_last_accessed"],
            'id': ["id"],
            'api_count': ["api_count"],
            'embed_count': ["embed_count"],
            'public_count': ["public_count"],
            'schedule_count': ["schedule_count"],
            'other_count': ["other_count"],
            'last_accessed_time': ["last_accessed_time"],
        }
        self.processed_message = self.transform()

    """
    Original:
    [{'content_usage.content_id': '181', 'content_usage.content_title': 'Taxi Streaming Demo', 'content_usage.content_type': 'dashboard', 'content_usage.days_since_last_access_tiers': '0 to 6', 'content_usage.days_since_last_accessed': 1, 'content_usage.id': 554, 'content_usage.api_count': 0, 'content_usage.embed_count': 0, 'content_usage.public_count': 0, 'content_usage.schedule_count': 0, 'content_usage.other_count': 7, 'content_usage.last_accessed_time': '2023-06-20 01:42:26'}]
    """
    def pre_processed(self, raw_message):
        if (not raw_message):
            return
        
        pre_processed_message = f"{{'result': {raw_message} }}"
        pre_processed_message = pre_processed_message\
                .replace("content_usage.", "")\
                .replace("'", '"')
            
        # handle case where the text has apostrophe (e.g 's)
        pattern = r'[^: ]"((\w{1})\s)'
        replace = r"'\1"
        pre_processed_message = re.sub(pattern, replace, pre_processed_message)
        return pre_processed_message

    """
    Raw: 
    {
        "result": [{'content_id': '181', 'content_title': 'Taxi Streaming Demo', 'content_type': 'dashboard', 'days_since_last_access_tiers': '0 to 6', 'days_since_last_accessed': 1, 'id': 554, 'api_count': 0, 'embed_count': 0, 'public_count': 0, 'schedule_count': 0, 'other_count': 7, 'last_accessed_time': '2023-06-20 01:42:26'}]
    }

    Processed:
    {
        "result": [{'content_id': '181', 'content_title': 'Taxi Streaming Demo', 'content_type': 'dashboard', 'days_since_last_access_tiers': '0 to 6', 'days_since_last_accessed': 1, 'id': 554, 'api_count': 0, 'embed_count': 0, 'public_count': 0, 'schedule_count': 0, 'other_count': 7, 'last_accessed_time': '2023-06-20 01:42:26'}]
    }
    """
    def transform(self):
        try:
            json_obj = json.loads(self.raw_message)
            mapped_obj = JsonMapper(json_obj).map(self.specification)
            return mapped_obj
        except Exception as e:
            print(f"Processing: unable to parse raw message due to {e}")
            print(f"Processing: message with error - {self.raw_message}")
            return []