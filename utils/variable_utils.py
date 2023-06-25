import json

def convert_bq_schema_to_string(schema: str) -> list:
    if not schema:
        return []
    try:
        formatted_schema = schema.replace("'", '"')
        formatted_list = f"[{formatted_schema}]"
        return json.loads(formatted_list)
    except Exception as e:
        print(f"Processing: Generating Schema Fails due to {e}")
        return []
    
def convert_string_to_bool(string_value: str) -> bool:
    if not string_value:
        return False
    
    return string_value.lower() == "true"

def convert_string_to_list(string_value: str, string_separator: str = ",") -> list:
    if not string_value:
        return []
    
    return string_value.split(string_separator)