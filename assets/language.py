from assets.work_with_files import read_json_file
#from random import choice
from assets.root import logger

class Language:
    def __init__(self, language:str):
        self.load_language(language)

    def load_language(self, language:str):
        self.language_name = language
        self.language = read_json_file(f"data/languages/{language}.json")
    
    def get(self, key: str) -> str:
        if key == "":
            return key

        if " " in key:
            return self._translate_multiple_keys(key.split(":"))
        else:
            if key[0] == "*":
                return key[1:]
            translate = self.language.get(key, None)
            if translate is None:
                self.language[key] = key
                logger.error(f"Key '{key}' not found in language '{self.language_name}'", f"Language.get({key})")
                return key
            else:
                return translate
    
    def _translate_multiple_keys(self, keys: list) -> str:
        data = ""
        for key in keys:
            if key == "":
                translate = key
            elif key[0] == "*":
                translate = key[1:]
            else:
                translate = self.language.get(key, None)

            if translate is None:
                logger.error(f"Key '{key}' not found in language '{self.language_name}'", f"Language._translate_multiple_keys({keys})")
                self.language[key] = key
                data += f" {key}"
            else:
                data += f" {translate}"
        return data