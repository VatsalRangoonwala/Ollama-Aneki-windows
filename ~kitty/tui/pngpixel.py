from pathlib import Path

from PIL import Image
from rich import print as rprint


class pngPix:
    def __init__(self, height, width, highlight, alert, normal):
        self.height = height
        self.width = width
        self.highlight = highlight
        self.alert = alert
        self.normal = normal
        self.dLowResPath = "saves/default/lowres/"
        self.dHighResPath = "saves/default/exp/"
        self.cLowResPath = "saves/custom/lowres/"
        self.cHighResPath = "saves/custom/exp/"
        self.emotions = [
            "angry",
            "confident",
            "confused",
            "curious",
            "happy",
            "nervous",
            "normal",
            "sad",
            "shy",
        ]

    def lower_resolution(self):

        # created libraries for default and custom

        Path(self.cLowResPath).mkdir(parents=True, exist_ok=True)
        Path(self.dLowResPath).mkdir(parents=True, exist_ok=True)
        Path(self.cHighResPath).mkdir(parents=True, exist_ok=True)

        try:
            rprint(f"{self.normal}Searching for custom images...")
            # Chceking wherether every emotion exist or not
            # If it does not exist, the program will move to default
            for emotion in self.emotions:
                image = Image.open(self.cHighResPath + emotion + ".png")
            rprint(f"{self.alert}Custom images found...  ")
            rprint(
                f"{self.highlight}Converting custom images in {self.height}x{self.width}... "
            )
            for emotion in self.emotions:
                # open image in high res
                image = Image.open(self.cHighResPath + emotion + ".png")
                # connvert it to low res
                new_image = image.resize((self.height, self.width))

                # save it
                new_image.save(f"{self.cLowResPath}{emotion}.png")
        except:
            rprint(f"{self.alert}NO custom images found...")
            rprint(
                f"{self.highlight}Converting default images in {self.height}x{self.width}..."
            )
            for emotion in self.emotions:
                # open image in high res
                image = Image.open(self.dHighResPath + emotion + ".png")
                # connvert it to low res
                new_image = image.resize((self.height, self.width))

                # save it
                new_image.save(f"{self.dLowResPath}{emotion}.png")
