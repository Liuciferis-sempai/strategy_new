import pygame as py

py.init()
py.font.init()

import assets.root as root
from assets.root import logger
from assets.functions import update_gui

def main():
    clock = py.time.Clock()

    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                logger.write_down()
                running = False
            elif event.type == py.VIDEORESIZE:
                root.window_size = event.w, event.h
                root.screen = py.display.set_mode(root.window_size, py.RESIZABLE)
                root.game.update_positions()
                update_gui()
            elif event.type == py.MOUSEMOTION:
                root.game.input_processor.process_mousemotion(event)
            elif event.type == py.MOUSEBUTTONDOWN:
                root.game.input_processor.process_mousebuttondown(event)
            elif event.type == py.KEYDOWN:
                root.game.input_processor.process_keydown(event)
            elif event.type == py.KEYUP:
                root.game.input_processor.process_keyup(event)
            elif event.type == py.MOUSEBUTTONUP:
                root.game.input_processor.process_mousebuttonup(event)

        if root.game.input_processor.is_move_button_pressed():
            root.game.input_processor.move()

        if root.need_update_gui:
            root.game.gui.draw()
        else:
            logger.write_down()

        py.display.update()

        clock.tick(root.config["FPS"])
        print(f"FPS: {clock.get_fps():.2f}\r", end="")
        #fps = int(clock.get_fps())
        #py.display.set_caption(f"FPS: {fps}")

if __name__ == "__main__":
    root.start_the_game("Test Game")
    main()
    py.quit()