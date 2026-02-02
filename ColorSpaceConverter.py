from PIL import Image


# Use this class to mainly convert from RGB --> YCbCr
class ColorSpaceConverter:
    def __init__(self, color_from, color_to):
        self.color_from = color_from
        self.color_to = color_to

    def convert(self, image: Image.Image) -> Image.Image:
        image = image.convert(self.color_from)
        return image.convert(self.color_to)

