class ZigZagScanner:
    def zigzag_all_blocks(self, Y_blocks, Cb_blocks, Cr_blocks):
        for channel_blocks in (Y_blocks, Cb_blocks, Cr_blocks):
            for blocks in channel_blocks:
                for block in blocks:
                    self.__zigzag_block(block)

    def __zigzag_block(self, block):
        if(block.shape[0] != block.shape[1]):
            raise ValueError(f"Block size is not square! {block.shape}")

        block_size = block.shape[0]
        print("Block_size: ", block_size)


