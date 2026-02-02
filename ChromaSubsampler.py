from PIL import Image

# Use this class for chroma subsampling
class ChromaSubsampler:
    def __init__(self, image: Image.Image, Y: int, Cb: int, Cr: int):
        if(image.mode != "YCbCr"):
            raise ValueError(f"Expected image in YCbCr mode, got {image.mode}")