import numpy as np

class ZigZagScanner:
    # Perform the zigzag scan for all channels
    def zigzag_all_blocks(self, Y_blocks, Cb_blocks, Cr_blocks):
        # Force block values to be integers
        Y_blocks = Y_blocks.astype(np.int32)
        Cb_blocks = Cb_blocks.astype(np.int32)
        Cr_blocks = Cr_blocks.astype(np.int32)

        scans = []

        for channel_blocks in (Y_blocks, Cb_blocks, Cr_blocks):
            channel_scan = []
            for blocks in channel_blocks:
                for block in blocks:
                    channel_scan.append(self.__zigzag_block(block))
            scans.append(channel_scan)
        return scans

    # Perform the zigzag scan: Go up, if the diagonal has an even index, and
    # go down, if it has an odd index --> keep direction changes in mind at all times!
    def __zigzag_block(self, block):
        if(block.shape[0] != block.shape[1]):
            raise ValueError(f"Block size is not square! {block.shape}")

        block_size = block.shape[0]
        scan = []
        # The number of diagonals is block_size * 2 - 1 --> for 8x8 blocks = 15
        num_diagonals = 2 * block_size - 1
        # Iterate over diagonals 0 to 14 and keep their direction in mind!
        for diagonal in range(num_diagonals):
            if(diagonal % 2 == 0):
                # even diagonals go bottom-up
                for i in range(diagonal + 1):
                    j = diagonal - i
                    if i < block_size and j < block_size:
                        # traverse from bottom-left to top-right --> swap indices!
                        # the bigger i(column) --> the smaller j(row) --> approaching top-right-corner
                        scan.append(block[j, i])
                        #print(f"EVEN i={j}, j={i}")
            else:
                # odd diagonals go top-down
                for i in range(diagonal + 1):
                    j = diagonal - i
                    if i < block_size and j < block_size:
                        # traverse from top-right to bottom-left --> keep indices in order!
                        # the bigger i(row) --> the smaller j(column) --> approaching bottom-left-corner
                        scan.append(block[i, j])
                        #print(f"ODD i={i}, j={j}")

        #print(f"Scan_shape: {len(scan)}, Scan: {np.array(scan).flatten().tolist()}")
        return scan


