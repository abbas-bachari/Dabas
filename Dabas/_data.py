
import json



class Data:
    def __init__(self, result:list ) -> None:
        self.result = result if result else []  # Check if result is empty

    def to_dict(self) -> list[dict]:
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

    def to_json(self, save_to_file:str=None)-> str:
        """Convert result list to JSON and save to file if specified"""
        try:
            json_data = json.dumps(self.to_dict(), indent=4)
            if save_to_file:
                with open(save_to_file, "w", encoding="utf-8") as f:
                    f.write(json_data)
                
            return json_data
        except Exception as e:
            print(f"❌ Error converting to JSON: {e}")
            return "{}"