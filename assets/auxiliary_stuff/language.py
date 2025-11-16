from .work_with_files import read_json_file
from .functions import can_be_int
import assets.root as root

class Language:
    def __init__(self, language:str):
        self.load_language(language)

    def load_language(self, language:str):
        self.language_name = language
        self.language = read_json_file(f"data/languages/{language}.json")
    
    def get(self, value: str) -> str:
        if value == "" or can_be_int(value):
            return value

        data = ""
        for key in value.split(" "):
            translate = self._translate_key(key)
            data += f"{translate} "
        return data
    
    def _translate_key(self, key: str) -> str:
        if key == "":
            return key
        elif key[0] == "*":
            return key[1:]
        elif can_be_int(key):
            return key
        else:
            translate = self.language.get(key, "__unknow__")
            if translate == "__unknow__":
                self.language[key] = key
                root.logger.error(f"Key '{key}' not found in language '{self.language_name}'", f"Language.get({key})")
                return key
            else:
                return translate