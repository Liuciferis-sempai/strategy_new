from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
import assets.root as root
from assets.root import logger

class GUIWriting:
    def __init__(self):
        self.writing = "" #type of input
        self.writing_index = 0
        
        self.all_input = []
        self.input = ""

    def start_writing(self):
        self.writing_index = 0
        self._set_titles()
        self.open()
        self.update_input_field()
        self.submit_button = InputSubmitButton()
    
    def submit_input(self):
        if self.writing_index < len(self.titles) - 1:
            self.writing_index += 1
            self.all_input.append(self.input)
            self.input = ""
            self.open()
        else:
            self.all_input.append(self.input)
            self.input = ""
            self.close(True)

    def _set_titles(self):
        match self.writing:
            case "Fraction Name":
                self.titles = ["Fraction Name", "Symbol", "Color"]
            case _:
                logger.error(f"Unknown writing type: {self.writing}", "GUIWriting._set_titles()")

    def _save_fraction_name(self):
        color = [255, 255, 255]
        try:
            full_color = [int(c) for c in self.all_input[2].split(" ")]
            color = full_color
        except ValueError:
            color = [255, 255, 255]
        data = {
            "set": True,
            "name": self.all_input[0],
            "symbol": self.all_input[1],
            "color": color
        }
        root.game_manager.fraction_manager.edit_fraction(id=root.player_id, data=data)
    
    def update_input_field(self):
        self.input_field = py.font.Font(None, 30).render(self.input, False, (0, 0, 0))
        self.input_field_bg = py.Surface((self.input_field.get_width() + 10, self.input_field.get_height() + 10))
        self.input_field_bg.fill((255, 255, 255))
        update_gui()
    
    def open(self):
        if self.writing != "":
            self.title = py.font.Font(None, 30).render(self.titles[self.writing_index], False, (255, 255, 255))
            self.update_input_field()
    
    def close(self, need_saving:bool=True):
        if need_saving:
            match self.writing:
                case "Fraction Name":
                    self._save_fraction_name()
                case _:
                    pass
        root.back_window_state()
        root.game_manager.gui.fraction.open_player_fraction()
        update_gui()
    
    def draw(self):
        root.screen.fill((0, 0, 0))

        root.screen.blit(self.title, (50, root.window_size[1]//2 - self.title.get_height()//2))
        root.screen.blit(self.input_field_bg, (50 + self.title.get_width() + 5, root.window_size[1]//2 - self.input_field.get_height()//2 - 5))
        root.screen.blit(self.input_field, (50 + self.title.get_width() + 10, root.window_size[1]//2 - self.input_field.get_height()//2))
        self.submit_button.change_position((root.window_size[0] - self.submit_button.width - 50, root.window_size[1]//2 - self.submit_button.height//2))
        root.screen.blit(self.submit_button.image, self.submit_button.rect)

        root.need_update_gui = False