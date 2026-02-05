from PIL import Image
import numpy

# Use this class for chroma subsampling
class ChromaSubsampler:
    # Expects an YCbCr image
    # Y: Luma subsampling factor
    # Ch: Horizontal chroma sampling factor
    # Cv: Vertical chroma sampling factor

    def __init__(self, image: Image.Image, Y: int, Ch: int, Cv: int):
        # Check for color space
        if(image.mode != "YCbCr"):
            raise ValueError(f"Expected image in YCbCr mode, got {image.mode}")

        # Check for valid subsampling values
        if ((Y, Ch, Cv) not in [(4, 4, 4), (4, 2, 2), (4, 2, 0)]):
            raise ValueError(f"Chroma subsampling can be 4:4:4, 4:2:2, or 4:2:0 for YCbCr")

        # If no errors occurred, initialize
        self.image = image
        self.Y, self.Ch, self.Cv = Y, Ch, Cv


    def subsample(self):
        Y, Cb, Cr = self.__convert_channels_to_arrays()

        # 4:4:4 → no chroma subsampling at all
        if (self.Y, self.Ch, self.Cv) == (4, 4, 4):
            print(f"Y: {Y.shape}, Cb: {Cb.shape}, Cr: {Cr.shape}")
            return Y, Cb, Cr

        # 4:2:2 → keep each row, but only every 2nd column
        if(self.Y, self.Ch, self.Cv) == (4, 2, 2):
            Cb = Cb[:, ::2]
            Cr = Cr[:, ::2]

        # 4:2:0 → keep only every 2nd row AND only every 2nd column
        if(self.Y, self.Ch, self.Cv) == (4, 2, 0):
            Cb = Cb[::2, ::2]
            Cr = Cr[::2, ::2]

        print(f"Y: {Y.shape}, Cb: {Cb.shape}, Cr: {Cr.shape}")
        return Y, Cb, Cr



    # Use this 'private' method for converting color channels to arrays
    # --> easier to use/manipulate further
    def __convert_channels_to_arrays(self):
        Y, Cb, Cr = self.image.split()
        return numpy.array(Y), numpy.array(Cb), numpy.array(Cr)