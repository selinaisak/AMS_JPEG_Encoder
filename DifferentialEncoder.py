class DifferentialEncoder:

    # Perform differential coding on DC coefficients of zigzag scanned blocks.
    # Each block’s DC coefficient is replaced by the difference from the previous block.
    def differential_encode(self, Y_scan, Cb_scan, Cr_scan):
        Y_diff = self.__diff_channel(Y_scan)
        Cb_diff = self.__diff_channel(Cb_scan)
        Cr_diff = self.__diff_channel(Cr_scan)
        return Y_diff, Cb_diff, Cr_diff

    def __diff_channel(self, channel_scan):
        # Perform differential coding for a single channel first
        diff_scans = []
        prev_dc = 0  # assume 0 for the first block
        for i, block_scan in enumerate(channel_scan):
            original_dc = block_scan[0]
            # first block keeps its initial value --> others will be
            # differential coded!
            diff_dc = original_dc - prev_dc
            # set original dc value to differential coded dc value
            block_scan[0] = diff_dc
            # add modified block
            diff_scans.append(block_scan)
            # swap dc for next run
            prev_dc = original_dc
            print(f"Block {i}: DC={original_dc} -> diff={diff_dc}")
        return diff_scans
