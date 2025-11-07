import pygame as py
import assets.root as root
import os
from assets.root import loading, logger

class ImageManager:
    def __init__(self):
        self.images = {}
        self.worldcell_images = {}
        self.cell_sizes= {i: size for i, size in enumerate(root.cell_sizes)}
        loading.draw("Loading images...")
        self.load_images()
        loading.draw("Transforming worldcell images...")
        self.transform_worldcell_images()

    def load_images(self):
        self.images = {}
        for filedir in os.listdir("data"):
            if os.path.isdir(f"data/{filedir}"):
                self._open_dir(f"data/{filedir}")

    def _open_dir(self, dir_path: str):
        for item in os.listdir(dir_path):
            full_path = f"{dir_path}/{item}"
            if os.path.isdir(full_path):
                self._open_dir(full_path)
            else:
                if item.endswith(".png"):
                    try:
                        image = py.image.load(full_path)
                        self.images[full_path] = image
                    except Exception as e:
                        logger.error(f"Failed to load image '{full_path}': {e}", f"ImageManager._open_dir(...)")
    
    def transform_worldcell_images(self):
        for size_key, size_value in self.cell_sizes.items():
            for image_path, image in self.images.items():
                if "data/map/cells_img" in image_path:
                    transformed_image = py.transform.scale(image, size_value)
                    self.worldcell_images[f"{image_path.replace("data/map/cells_img/", "")}_worldcell_{size_key}"] = transformed_image 

    def get_image(self, image_path: str, none_path: str="data/icons/none.png") -> py.Surface:
        image = self.images.get(image_path, None)
        if image is None:
            logger.error(f"Image '{image_path}' not found in ImageManager", f"ImageManager.get_image(...)")
            image = self.images.get(none_path, None)
            if image is None:
                logger.error(f"None image '{none_path}' not found in ImageManager", f"ImageManager.get_image(...)")
                try:
                    return py.image.load(image_path)
                except Exception as e:
                    logger.error(f"Failed to load image '{image_path}': {e}", f"ImageManager.get_image(...)")
                    try:
                        return py.image.load(none_path)
                    except Exception as e:
                        logger.error(f"Failed to load none image '{none_path}': {e}", f"ImageManager.get_image(...)")
                        return py.image.load("data/icons/none.png")
            else:
                self.images[image_path] = py.image.load(none_path)
        return image.copy()
    
    def get_worldcell_image(self, image_name: str, none_cat: str) -> py.Surface:
        key = f"{image_name}_worldcell_{root.cell_size_scale}"
        image = self.worldcell_images.get(key, None)
        if image is None:
            logger.error(f"Worldcell image '{key}' not found in ImageManager", f"ImageManager.get_worldcell_image(...)")
            return self.get_image(image_name, f"data/map/cells_img/{none_cat}/none.png")
        return image.copy()