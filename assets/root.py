from .auxiliary_stuff import *
#Clear logs
write_txt_file("data/logs.txt", "")
write_txt_file("data/errors.txt", "")

from .helpers.logger import Logger
logger = Logger()

#pygame load
import pygame as py
screen = py.display.set_mode((800, 600), py.RESIZABLE)
#py.display.set_caption("My Game")
py.display.set_caption("MyCountry")

from .helpers.loading import Loading
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
food_sufficiency_factor_frame = (0, 1.2)
food_sufficiency_factor_center = 0.6
river_count = 10
time_for_show_info = 60

#Variables
window_state = "game"
last_window_state = "game"
player_id = 0
year_length = 1
base_growth_rate = 0.35
base_mortality_rate_aged = 0.4
base_mortality_rate_adult = 0.1
base_mortality_rate_children = 0.05
food_valued_consumption_per_person_factor = 1

#Boolean
running = True
need_update_gui = True
input_field_active = False

#Resize window
screen = py.display.set_mode(window_size, py.RESIZABLE)

loading.draw("Config loading...")
#config load
config = read_json_file("data/config.json")
cell_size_scale = config.get("cell_size_scale", 1)

from .helpers.language import Language
language = Language(config["language"])

loading.draw("Image manager initializing...")
from .managers.image_manager import ImageManager
image_manager = ImageManager()

loading.draw("Game initializing...")
from .gamemanager import GameManager
game_manager = GameManager()
game_manager.initialize()
game_manager.gui.change_position_for_new_screen_sizes()