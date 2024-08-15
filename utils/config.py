import yaml
import json
from typing import Dict, Any



def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)
    

def load_config(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def save_config(file_path: str, config: Dict[str, Any]) -> None:
    with open(file_path, 'w') as file:
        yaml.dump(config, file)

def update_config() -> Dict[str, Any]:
    print("Please enter the configuration details.")

    request_interval = float(input("Interval between requests (seconds): "))
    sentence_length = int(input("Length of fake sentence: "))
    endpoints = input("Comma-separated list of endpoints: ").split(",")

    return {
        "request_interval": request_interval,
        "sentence_length": sentence_length,
        "endpoints": endpoints
    }
