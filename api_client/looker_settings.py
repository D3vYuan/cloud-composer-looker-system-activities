from looker_sdk import api_settings
from airflow.models import Variable

class LookSettings(api_settings.ApiSettings):
    
    # https://github.com/looker-open-source/sdk-codegen/tree/main/python#configuring-the-sdk
    def __init__(self, *args, **kw_args):
        self.mode = kw_args.pop("mode")
        super().__init__(*args, **kw_args)

    # https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/variables.html
    def read_config(self) -> api_settings.SettingsConfig:
        config = super().read_config()
        # See api_settings.SettingsConfig for required fields
        if self.mode == "api_config":
            config["client_id"] = Variable.get("looker_api_client_id", default_var="")
            config["client_secret"] = Variable.get("looker_api_client_secret", default_var="")
            config["base_url"] = Variable.get("looker_api_base_url", default_var="")
            config["verify_ssl"] = Variable.get("looker_api_verify_ssl", default_var="false")
            config["timeout"] = Variable.get("looker_api_timeout", default_var=120)
        return config
    
if __name__ == '__main__':
    config = LookSettings(mode="api_config")