from api_client.looker_settings import LookSettings
import looker_sdk
import os

class Connection():
    def __init__(self, config_file="../looker.ini") -> None:
        self.config_file = config_file
        self.sdk = self.generate_connection()

    def generate_connection(self):
        hostname = os.uname()[1]
        if "airflow-worker" not in hostname:
            return looker_sdk.init40(self.config_file)
        else:
            return looker_sdk.init40(config_settings=LookSettings(mode="api_config"))