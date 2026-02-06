import numpy as np

# Source (quantization tables): https://www.sciencedirect.com/topics/engineering/quantization-table
# Source (quality factor): https://stackoverflow.com/questions/29215879/how-can-i-generalize-the-quantization-matrix-in-jpeg-compression

L = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
], dtype=np.int32)

C = np.array([
    [17, 18, 24, 47, 99, 99, 99, 99],
    [18, 21, 26, 66, 99, 99, 99, 99],
    [24, 26, 56, 99, 99, 99, 99, 99],
    [47, 66, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99]
], dtype=np.int32)

class Quantizer:
    def __init__(self, q_factor):
        # This factor can range from 1 to 100
        if(q_factor < 1 or q_factor > 100):
            raise ValueError("Quantizer factor must be between 1 and 100")
        self.q_factor = q_factor

    # Quantize all blocks using scaling of quantization tables + q_factor
    def quantize_blocks(self, Y_blocks, Cb_blocks, Cr_blocks):

        luma_h, luma_w, _, _ = Y_blocks.shape

        for i in range(luma_h):
            for j in range(luma_w):
                Y_blocks[i, j] = self.__quantize_block(Y_blocks[i, j], L)

        chroma_h, chroma_w, _, _ = Cb_blocks.shape
        for i in range(chroma_h):
            for j in range(chroma_w):
                Cb_blocks[i, j] = self.__quantize_block(Cb_blocks[i, j], C)
                Cr_blocks[i, j] = self.__quantize_block(Cr_blocks[i, j], C)
        #print("Q_V: ", Y_blocks)
        #print("Q_Cb: ", Cb_blocks)
        #print("Q_Cr: ", Cr_blocks)
        return Y_blocks, Cb_blocks, Cr_blocks

    # Scale the tables according to the quality factor --> return integer array
    def __quantize_block(self, block, table):
        scaled_table = self.__scale_table(table)
        return np.round(block/scaled_table).astype(dtype=np.int32)

    # Calculate scaled tables according to quality factor
    def __scale_table(self, table):
        # 1 <= q_factor < 50 = range(102, 5000) [for scale]
        if(self.q_factor < 50):
            scale = 5000 / self.q_factor
        else:
            # 50 <= q_factor <= 100 = range(0, 100) [for scale]
            scale = 200 - 2 * self.q_factor

        # range(0.5, 50.5) --> floor  = range (0, 50) [ignoring table]
        scaled_table = np.floor((table * scale + 50) / 100)
        scaled_table[scaled_table == 0] = 1  # avoid zeros --> for later division!
        return scaled_table
