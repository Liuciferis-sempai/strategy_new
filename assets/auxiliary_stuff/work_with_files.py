import json
from typing import Any

def open_txt_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        data = file.read()
    
    return data

def write_txt_file(file_path: str, data: str):
    with open(file_path, "w") as file:
        file.write(data)

def read_json_file(file_path: str) -> dict[str, Any]:
    with open(file_path, "r") as file:
        data = json.load(file)
    
    return data

def write_json_file(file_path:str, data:dict[str, Any]|list[str]):
    '''
    use as data one dict if you want to write full new data
    or as data a list of two strings if you want to change one value or add new one to the file
    '''
    if data is dict: #write full new data
        _write_json_file(file_path, data)
    elif data is str: #change one value or add new one
        with open(file_path, "r") as file:
            file_data = json.load(file)
        for key, _ in file_data.items():
            if key == data[0]:
                file_data[key] = data[1]
                _write_json_file(file_path, file_data)
                return
        else:
            file_data[data[0]] = data[1]
            _write_json_file(file_path, file_data)
                
def _write_json_file(file_path:str, data:dict[str, Any]):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)