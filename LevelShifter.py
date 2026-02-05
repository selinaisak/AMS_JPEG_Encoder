class LevelShifter:
    def __init__(self, level):
        self.level = level

    def shift(self, Y_blocks, Cb_blocks, Cr_blocks):
        for channel_blocks in (Y_blocks, Cb_blocks, Cr_blocks):
            for blocks in channel_blocks:
                for block in blocks:
                    print(block.shape)
                    pass

        return []