import numpy as np

class BlockSplitter:
    # Expects a block size
    def __init__(self, block_size):
        self.block_size = block_size

    # Split the channel into block_size x block_size blocks
    # --> keep private
    def __split_channel(self, channel: np.ndarray):
        h, w = channel.shape

        # Calculate necessary padding
        # 1st: self.block_size - h % self.block_size --> calculate how many rows/columns must
        #      be added to reach a multiple of block_size
        # 2nd: in case it is already a multiple of block_size --> step 1 would result in
        #      additionally <block_size> needed rows/columns, example: (8 - h%8) = (8 - 0) = 8
        #      --> therefore add %block_size again --> resulting in 0 padding needed
        pad_h = (self.block_size - h % self.block_size) % self.block_size
        pad_w = (self.block_size - w % self.block_size) % self.block_size

        # Pad the edges by repeating the last row/column --> mode='edge':
        # Pads with the edge values of array
        padded_channel = np.pad(channel, ((0, pad_h), (0, pad_w)), mode='edge')

        # Overwrite h and w with new values
        h, w = padded_channel.shape

        # Reshape into blocks: first split rows and columns into block_size chunks
        blocks = padded_channel.reshape(h // self.block_size, self.block_size,
                                        w // self.block_size, self.block_size)

        # Reorganize block axes: (num_blocks_vertical, num_blocks_horizontal, block_size, block_size)
        blocks = blocks.transpose(0, 2, 1, 3)

        return blocks

    # Use this 'public' method for splitting all channels into blocks
    def split_all_channels(self, Y: np.ndarray, Cb: np.ndarray, Cr: np.ndarray):
        Y_blocks = self.__split_channel(Y)
        Cb_blocks = self.__split_channel(Cb)
        Cr_blocks = self.__split_channel(Cr)
        return Y_blocks, Cb_blocks, Cr_blocks
