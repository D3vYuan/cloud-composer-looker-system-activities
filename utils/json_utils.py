import jsonlines

def convert_json_to_jsonl(data, destination_file) -> bool:
    if not data:
        return False
    
    try:
        with jsonlines.open(destination_file, 'w') as writer:
            writer.write_all(data)
            return True
    except Exception as e:
        print(f"Processing: Saving json to {destination_file} fails due to {e}")
    return False

