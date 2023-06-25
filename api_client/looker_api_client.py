import sys
sys.path.append('..')

import traceback
from datetime import datetime
from api_client.looker_look_query import LookQuery
from api_client.looker_output import LookOutput
from transformation.content_usage_transformation import ContentUsageTransformation
from parameters.content_usage_parameters import ContentUsageParams

def get_content_usage_look(execution_timestamp, id = None, 
                           data_fields = None, data_filters = None,
                           initial_load = False):
    try:
        look_params = ContentUsageParams(execution_timestamp = execution_timestamp, 
                                         id = id, data_fields = data_fields,
                                         data_filters = data_filters, initial_load = initial_load)
        print(f"Processing: Retrieving information for Look #{look_params.id}")
        look_query = LookQuery(look_params)
        look_query_result = look_query.execute()
        # print(f"{look_query_result}")
        print(f"Processing: Found {len(look_query_result)} records for Look #{look_params.id}")

        look_result_transformation = ContentUsageTransformation(look_query_result)
        look_json = look_result_transformation.processed_message
        
        look_output = LookOutput(json_data = look_json,
                                filename_prefix = "content_usage", 
                                execution_timestamp = execution_timestamp)
        save_status = look_output.save()
        print(f"Processing: Records saved to {look_output.file_path.absolute()} for Look #{look_params.id} - [{save_status}]")
        return str(look_output.file_path.absolute())
    except Exception as e:
        print(f"Processing: Failed to get system activity due to {e}")
        traceback.print_exc()
    return ""

if __name__ == "__main__":
    # current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    current_timestamp = datetime.now().strftime("%Y%m%d")
    get_content_usage_look(current_timestamp, initial_load = True)
    