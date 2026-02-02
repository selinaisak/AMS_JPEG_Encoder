from PIL import Image

# Use this class for chroma subsampling
class ChromaSubsampler:
    # Expects an YCbCr image
    # Y: Luma value
    # Cb: Blue chroma value
    # Cr: Red chroma value

    def __init__(self, image: Image.Image, Y: int, Cb: int, Cr: int):
        # Check for color space
        if(image.mode != "YCbCr"):
            raise ValueError(f"Expected image in YCbCr mode, got {image.mode}")

        # Check for valid subsampling values
        if ((Y, Cb, Cr) not in [(4, 4, 4), (4, 2, 2), (4, 2, 0)]):
            raise ValueError(f"Chroma subsampling can be 4:4:4, 4:2:2, or 4:2:0 for YCbCr")

        # If no errors occurred, initialize
        self.image = image
        self.Y, self.Cb, self.Cr = Y, Cb, Cr