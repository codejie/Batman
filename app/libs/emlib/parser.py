from typing import Any, Dict, List, Optional, Union
from pandas import DataFrame

class EMParser:
    """
    Data parser for EastMoney API responses.
    This class handles the analysis and reassembly of raw data.
    """
    
    @staticmethod
    def extract_list(data: Dict[str, Any], path: str = "data") -> List[Any]:
        """
        Extract a list of items from a nested dictionary based on a simple path.
        """
        keys = path.split(".")
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return []
        
        return current if isinstance(current, list) else []

    @staticmethod
    def to_dataframe(data: List[Dict[str, Any]], rename_map: Optional[Dict[str, str]] = None) -> DataFrame:
        """
        Convert a list of items to a pandas DataFrame and rename columns if needed.
        """
        df = DataFrame(data)
        if rename_map and not df.empty:
            df.rename(columns=rename_map, inplace=True)
        return df

    @staticmethod
    def reassemble(data: List[Dict[str, Any]], field_map: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Reassemble each item in the list according to the specified field mapping.
        """
        reassembled = []
        for item in data:
            new_item = {}
            for raw_key, new_key in field_map.items():
                if raw_key in item:
                    new_item[new_key] = item[raw_key]
            reassembled.append(new_item)
        return reassembled

parser = EMParser()
