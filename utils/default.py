import json
import requests





def config(filename: str = "config"):
    try:
        with open(f"{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could Not find {filename}.json")
        
        
        
 
