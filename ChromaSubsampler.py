import numpy as np
from PIL import Image

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

        # 4:2:2 → reduce columns by half
        if(self.Y, self.Ch, self.Cv) == (4, 2, 2):
            # keep each row, but only every 2nd column
            #Cb = Cb[:, ::2]
            #Cr = Cr[:, ::2]
            # average pixel pairs across columns
            Cb = self.__subsample_422(Cb)
            Cr = self.__subsample_422(Cr)

        # 4:2:0 → reduce columns AND rows by half
        if(self.Y, self.Ch, self.Cv) == (4, 2, 0):
            # keep only every 2nd row AND only every 2nd column
            #Cb = Cb[::2, ::2]
            #Cr = Cr[::2, ::2]
            # average pixel blocks across columns AND rows (2x2 blocks)
            Cb = self.__subsample_420(Cb)
            Cr = self.__subsample_420(Cr)

        print(f"Y: {Y.shape}, Cb: {Cb.shape}, Cr: {Cr.shape}")
        return Y, Cb, Cr



    # Use this 'private' method for converting color channels to arrays
    # --> easier to use/manipulate further
    def __convert_channels_to_arrays(self):
        Y, Cb, Cr = self.image.split()
        return np.array(Y), np.array(Cb), np.array(Cr)

    # Use this 'private' method for 4:2:2 subsampling using averaging
    # --> build average of pixel pairs across columns, ex:
    # from:
    # [a, b, c, d,
    #  e, f, g, h] --> 2 x 4 shape
    #
    # to:
    # [(a+b)/2, (c+d)/2,
    #  (e+f)/2, (g+h)/2] --> 2 x 2 shape
    def __subsample_422(self, channel: np.ndarray):
        height, width = channel.shape
        # ensure even number of columns
        channel = channel[:, :width - (width % 2)]
        # reshape, so that 2 columns are grouped together for averaging their pixel pairs
        channel = channel.reshape(height, width // 2, 2)
        # average along axis=2 --> refers to the chroma pixel pairs
        return channel.mean(axis=2).astype(np.uint8)

    # Use this 'private' method for 4:2:0 subsampling using averaging
    # --> build average of 2 x 2 pixel blocks across columns AND rows, ex:
    # from:
    # [a, b, c, d,
    #  e, f, g, h] --> 2 x 4 shape
    #
    # to:
    # [(a+b+e+f)/4, (c+d+g+h)/4] --> 1x2 shape
    def __subsample_420(self, channel: np.ndarray):
        height, width = channel.shape
        # ensure even number of rows and columns
        channel = channel[:height - (height % 2), :width - (width % 2)]
        # reshape, so that pixel values are grouped together in a 2 x 2 block
        channel = channel.reshape(height // 2, 2, width // 2, 2)
        # average along axis 1 (horizontal grouping) and 3 (vertical grouping) --> in total
        # average across 2 x 2 block
        return channel.mean(axis=(1, 3)).astype(np.uint8)