from scipy.fftpack import dct
import numpy as np

def DCT_2D(Y_blocks, Cb_blocks, Cr_blocks):
    Y_blocks = Y_blocks.astype(np.float32)
    Cb_blocks = Cb_blocks.astype(np.float32)
    Cr_blocks = Cr_blocks.astype(np.float32)

    for channel_blocks in (Y_blocks, Cb_blocks, Cr_blocks):
        num_vertical, num_horizontal, block_height, block_width = channel_blocks.shape
        for i in range(num_vertical):
            for j in range(num_horizontal):
                channel_blocks[i, j] = __DCT_2D_per_block(channel_blocks[i, j])
    return Y_blocks, Cb_blocks, Cr_blocks

def __DCT_2D_per_block(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')
