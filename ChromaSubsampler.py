from PIL import Image

# Use this class for chroma subsampling
class ChromaSubsampler:
    def __init__(self, image: Image.Image, Y: int, Cb: int, Cr: int):
        if(image.mode != "YCbCr"):
            raise ValueError(f"Expected image in YCbCr mode, got {image.mode}")
        if ((Y, Cb, Cr) not in [(4, 4, 4), (4, 2, 2), (4, 2, 0)]):
            raise ValueError(f"Chroma subsampling can be 4:4:4, 4:2:2, or 4:2:0 for YCbCr")