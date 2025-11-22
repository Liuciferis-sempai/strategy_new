from ..auxiliary_stuff.work_with_files import read_json_file
from ..auxiliary_stuff.functions import can_be_int
from .. import root
from typing import Any

class Language:
    def __init__(self, language:str):
        self.load_language(language)

    def load_language(self, language:str):
        self.language_name = language
        self.language = read_json_file(f"data/languages/{language}.json")
    
    def get(self, translate_code: str, kwargs: dict[str, Any] = {}) -> str:
        if translate_code == "" or can_be_int(translate_code):
            return translate_code
        else:
            answer = ""
            to_translate = translate_code.split(" ")
            for word in to_translate:
                answer += f"{self._translate(word, **kwargs)} "
            return answer
    
    def _translate(self, translate_code: str, **kwargs) -> str:
        if "*" in translate_code: return translate_code.replace("*", "")

        translate_text = self.language.get(translate_code)
        if translate_text is not None:
            try:
                return translate_text.format(**kwargs)
            except KeyError:
                root.logger.error(f"not enough arguments for translation code {translate_code}", f"Language._translate({translate_code}, {kwargs})")
                return translate_text
        else:
            root.logger.error(f"can not find translation for code {translate_code}", f"Language._translate({translate_code}, {kwargs})")
            temp_translate = translate_code
            for key in kwargs.keys():
                temp_translate += " {" + key + "}"
            self.language[translate_code] = temp_translate

            return temp_translate.format(**kwargs)