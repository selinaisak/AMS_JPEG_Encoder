from PIL import Image
import numpy

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


    def subsample(self):
        Y, Cb, Cr = self.__convert_channels_to_arrays()
        print(f"Y: {Y.shape}, Cb: {Cb.shape}, Cr: {Cr.shape}")


    # Use this 'private' method for converting color channels to arrays
    # --> easier to use/manipulate further
    def __convert_channels_to_arrays(self):
        Y, Cb, Cr = self.image.split()
        return numpy.array(Y), numpy.array(Cb), numpy.array(Cr)