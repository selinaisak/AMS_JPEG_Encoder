class RunLengthEncoder:

    # Perform Run-Length Encoding for JPEG AC coefficients.
    # Input blocks must already be zigzag scanned and differential coded!
    def rl_encode(self, Y_diff, Cb_diff, Cr_diff):
        Y_rle = self.__rl_encode_channel(Y_diff)
        print(f"Y_rle: {Y_rle}")
        Cb_rle = self.__rl_encode_channel(Cb_diff)
        print(f"Cb_rle: {Cb_rle}")
        Cr_rle = self.__rl_encode_channel(Cr_diff)
        print(f"Cr_rle: {Cr_rle}")
        return Y_rle, Cb_rle, Cr_rle

    def __rl_encode_channel(self, channel_scan):
        # Perform RLE for a single channel first
        encoded_blocks = []
        for block_scan in channel_scan:
            encoded_blocks.append(self.__rl_encode_block(block_scan))
        return encoded_blocks

    def __rl_encode_block(self, block_scan):
        # Encode a single block
        # DC was differential coded already, now we need to take care of the AC values!
        # For RLE: keep track of 'zero runs' to improve compression efficiency


        # The first value is the DC value --> ignore for now
        # All the rest are AC values!
        dc = int(block_scan[0])
        ac = block_scan[1:]

        rle = []
        zero_run = 0

        for coefficient in ac:
            coefficient = int(coefficient)
            if coefficient == 0:
                zero_run += 1
                # 16 consecutive 0s --> "ZRL"
                if(zero_run == 16):
                    rle.append((15, 0))
                    zero_run = 0
            else:
                rle.append((zero_run, coefficient))
                zero_run = 0

        # End of Block (= EOB) if remaining coefficients are zero
        if zero_run > 0:
            rle.append((0, 0))  # EOB

        # Return dictionary with DC, and RLE AC values (separately)
        return {
            "DC": dc,
            "AC": rle
        }
