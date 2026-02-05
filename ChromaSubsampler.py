import numpy as np
from PIL import Image

# Use this class for chroma subsampling
class ChromaSubsampler:
    # Expects an YCbCr image
    # L: Luma subsampling factor
    # Ch: Horizontal chroma sampling factor
    # Cv: Vertical chroma sampling factor

    def __init__(self, image: Image.Image, L: int, Ch: int, Cv: int):
        # Check for color space
        if(image.mode != "YCbCr"):
            raise ValueError(f"Expected image in YCbCr mode, got {image.mode}")

        # Check for valid subsampling values
        if ((L, Ch, Cv) not in [(4, 4, 4), (4, 2, 2), (4, 2, 0)]):
            raise ValueError(f"Chroma subsampling can be 4:4:4, 4:2:2, or 4:2:0 for YCbCr")

        # If no errors occurred, initialize
        self.image = image
        self.L, self.Ch, self.Cv = L, Ch, Cv


    def subsample(self):
        Y, Cb, Cr = self.__convert_channels_to_arrays()

        # 4:4:4 → no chroma subsampling at all
        if (self.L, self.Ch, self.Cv) == (4, 4, 4):
            print(f"Y: {Y.shape}, Cb: {Cb.shape}, Cr: {Cr.shape}")
            return Y, Cb, Cr

        # 4:2:2 → reduce columns by half
        if(self.L, self.Ch, self.Cv) == (4, 2, 2):
            # keep each row, but only every 2nd column
            #Cb = Cb[:, ::2]
            #Cr = Cr[:, ::2]
            # average pixel pairs across columns
            Cb = self.__subsample_422(Cb)
            Cr = self.__subsample_422(Cr)

        # 4:2:0 → reduce columns AND rows by half
        if(self.L, self.Ch, self.Cv) == (4, 2, 0):
            # keep only every 2nd row AND only every 2nd column
            #Cb = Cb[::2, ::2]
            #Cr = Cr[::2, ::2]
            # average pixel blocks across columns AND rows (2x2 blocks)
            Cb = self.__subsample_420(Cb)
            Cr = self.__subsample_420(Cr)

        print(f"Y: {Y.shape}, Cb: {Cb.shape}, Cr: {Cr.shape}")
        return Y, Cb, Cr

    def upsample(self, Y, Cb, Cr):
        # 4:4:4 → no chroma subsampling at all
        if (self.L, self.Ch, self.Cv) == (4, 4, 4):
            print(f"Y: {Y.shape}, Cb: {Cb.shape}, Cr: {Cr.shape}")
            return Y, Cb, Cr
        if (self.L, self.Ch, self.Cv) == (4, 2, 2):
            Cb = self.__upsample_422(Cb, Y.shape)
            Cr = self.__upsample_422(Cr, Y.shape)

        if (self.L, self.Ch, self.Cv) == (4, 2, 0):
            Cb = self.__upsample_420(Cb, Y.shape)
            Cr = self.__upsample_420(Cr, Y.shape)

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


    def __upsample_422(self, channel, target_shape):
        h, w = target_shape
        return channel.repeat(2, axis=0)[:h, :w]

    def __upsample_420(self, channel, target_shape):
        h, w = target_shape
        upsampled = channel.repeat(2, axis=0).repeat(2, axis=1)[:h, :w]
        if(target_shape == upsampled.shape):
            return upsampled
        return self.__pad(upsampled, target_shape)

    def __pad(self, channel, target_shape):
        h, w = target_shape
        out = np.zeros(target_shape, dtype=channel.dtype)
        out[:channel.shape[0], :channel.shape[1]] = channel

        # Repeat last row if needed
        if channel.shape[0] < h:
            print("OUT: ", out.shape)
            print("CHANNEL: ", channel.shape)
            out[channel.shape[0]:, :channel.shape[1]] = channel[-1:, :]

        # Repeat last column if needed
        if channel.shape[1] < w:
            out[:, channel.shape[1]:] = out[:, channel.shape[1] - 1:channel.shape[1]]

        return out
