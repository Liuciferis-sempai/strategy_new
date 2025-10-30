from .work_with_files import write_txt_file
#Clear logs
write_txt_file("data/logs.txt", "")
write_txt_file("data/errors.txt", "")

from .logger import Logger
logger = Logger()

#pygame load
import pygame as py
screen = py.display.set_mode((800, 600), py.RESIZABLE)
#py.display.set_caption("My Game")
py.display.set_caption("MyCountry")

from .loading import Loading
loading = Loading()
loading.draw("Loading root module...")

#Global variables
#Sizes
window_size = (800, 600)
interface_size = 200
#cell_size_scale = 1 will be loaded from config
cell_sizes = [(20, 20), (50, 50), (75, 75), (100, 100), (125, 125), (150, 150), (175, 175), (200, 200)]
button_standard_size = (150, 50)
info_box_size = (75, 25)
world_map_size = (150, 150)
river_count = 10
time_for_info_show = 1000

#Variables
window_state = "game"
last_window_state = "game"
game_name = ""
player_id = 1
input = ""
all_input = []
input_field_active = False

#Boolean
need_update_gui = True

#Resize window
screen = py.display.set_mode(window_size, py.RESIZABLE)

loading.draw("Config loading...")
#config load
from .work_with_files import read_json_file
config = read_json_file("data/config.json")
cell_size_scale = config.get("cell_size_scale", 1)

from assets.language import Language
language = Language(config["language"])

loading.draw("Image manager initializing...")
from .image_manager.image_manager import ImageManager
image_manager = ImageManager()

loading.draw("Game initializing...")
from assets.gamemanager import GameManager
game_manager = GameManager()
game_manager.gui.initialize()
game_manager.gui.change_position_for_new_screen_sizes()

from .functions import *