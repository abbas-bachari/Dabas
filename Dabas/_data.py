import pandas as pd
import json



class Data:
    def __init__(self, result) -> None:
        self.result = result if result else []  # Check if result is empty

    def to_dict(self):
        """Convert result list to dictionary"""
        if not self.result:
            return []
        try:
            data_list = [item.__dict__ for item in self.result]
            for data in data_list:
                data.pop("_sa_instance_state", None)  # Remove extra column
            return data_list
        except Exception as e:
            print(f"❌ Error converting to dictionary: {e}")
            return []

    def to_json(self, save_to_file:str=None):
        """Convert result list to JSON and save to file if specified"""
        try:
            json_data = json.dumps(self.to_dict(), indent=4)
            if save_to_file:
                with open(save_to_file, "w", encoding="utf-8") as f:
                    f.write(json_data)
                print(f"✅ Data saved to {save_to_file}")
            return json_data
        except Exception as e:
            print(f"❌ Error converting to JSON: {e}")
            return "{}"

    def to_dataframe(self, index_key=None, datetime_keys=[]):
        """Convert result list to DataFrame and set index"""
        data_list = self.to_dict()
        if not data_list:
            return pd.DataFrame()

        try:
            df = pd.DataFrame(data_list)

            # convert datetime columns to datetime if exists
            for key in datetime_keys:
                if key in df.columns and df[key].notnull().all():
                    df[key] = pd.to_datetime(df[key], unit="ms")

            # set index to primary key
            if index_key and index_key in df.columns:
                df.set_index(index_key, inplace=True)

            return df
        except Exception as e:
            print(f"❌ Error converting to DataFrame: {e}")
            return pd.DataFrame()
