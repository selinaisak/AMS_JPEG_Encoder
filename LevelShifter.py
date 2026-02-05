import numpy as np

class LevelShifter:
    def __init__(self, level):
        self.level = level

    # Shift block values from [0, 255] to [-128,127] for DCT!
    def shift(self, Y_blocks, Cb_blocks, Cr_blocks):
        # Need to transform base datatype -->
        # from dtype=uint8 (unsigned 8-bit integers) to int16 -->
        # otherwise level shift will NOT work!
        Y_blocks = Y_blocks.astype(np.int16)
        Cb_blocks = Cb_blocks.astype(np.int16)
        Cr_blocks = Cr_blocks.astype(np.int16)
        for channel_blocks in (Y_blocks, Cb_blocks, Cr_blocks):
            for blocks in channel_blocks:
                for block in blocks:
                    h, w = block.shape
                    for i in range(h):
                        for j in range(w):
                            block[i, j] = block[i, j] - self.level
        self.__verify_blocks(Y_blocks, Cb_blocks, Cr_blocks)
        return Y_blocks, Cb_blocks, Cr_blocks

    # Just in case: Check whether all block values are in the target range!
    def __verify_blocks(self, Y_blocks, Cb_blocks, Cr_blocks):
        for channel_blocks in (Y_blocks, Cb_blocks, Cr_blocks):
            for blocks in channel_blocks:
                for block in blocks:
                    h, w = block.shape
                    for i in range(h):
                        for j in range(w):
                            if(127 < block[i, j] or block[i, j] < -128):
                                raise ValueError(f"Block value out of range! Value: {block[i, j]}")