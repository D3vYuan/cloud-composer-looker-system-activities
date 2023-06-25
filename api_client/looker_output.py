import sys
sys.path.append('..')

import os
from pathlib import Path

from utils.json_utils import convert_json_to_jsonl

class LookOutput():
    def __init__(self, json_data, execution_timestamp, 
                file_directory=None, 
                filename_prefix="system_activity", 
                filename_extension="jsonl"):
        self.json_data = json_data
        self.file_directory = self.generate_file_directory(file_directory)
        self.filename = f"{filename_prefix}_{execution_timestamp}.{filename_extension}"
        self.file_path = Path(self.file_directory, self.filename)

    def generate_file_directory(self, file_directory):
        hostname = os.uname()[1]
        if not file_directory and "airflow-worker" in hostname:
            return "/tmp"
        elif not file_directory and "airflow-worker" not in hostname:
            return "."
        else:
            return file_directory

    def save(self):
        return convert_json_to_jsonl(self.json_data, self.file_path.absolute())

