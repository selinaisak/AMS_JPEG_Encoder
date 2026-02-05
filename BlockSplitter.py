import numpy as np

class BlockSplitter:
    # Expects a block size
    def __init__(self, block_size):
        self.block_size = block_size

    # Split the channel into block_size x block_size blocks
    def split_channel(self, channel: np.ndarray):
        h, w = channel.shape

        # Calculate necessary padding
        # 1st: self.block_size - h % self.block_size --> calculate how many rows/columns must
        #      be added to reach a multiple of block_size
        # 2nd: in case it is already a multiple of block_size --> step 1 would result in
        #      additionally <block_size> needed rows/columns, example: (8 - h%8) = (8 - 0) = 8
        #      --> therefore add %block_size again --> resulting in 0 padding needed
        pad_h = (self.block_size - h % self.block_size) % self.block_size
        pad_w = (self.block_size - w % self.block_size) % self.block_size
        print("Padding: ", pad_h, pad_w)