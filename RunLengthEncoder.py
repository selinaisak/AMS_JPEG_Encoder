class RunLengthEncoder:

    # Perform Run-Length Encoding for JPEG AC coefficients.
    # Input blocks must already be zigzag scanned and differential coded!
    def rl_encode(self, Y_diff, Cb_diff, Cr_diff):
        # Encode each channel separately
        Y_rle = self.__rl_encode_channel(Y_diff)
        Cb_rle = self.__rl_encode_channel(Cb_diff)
        Cr_rle = self.__rl_encode_channel(Cr_diff)
        return Y_rle, Cb_rle, Cr_rle

    def __rl_encode_channel(self, channel_scan):
        # Encode all blocks in a single channel
        encoded_blocks = []
        for block_scan in channel_scan:
            encoded_blocks.append(self.__rl_encode_block(block_scan))
        return encoded_blocks

    def __rl_encode_block(self, block_scan):
        # DC coefficient (already differential coded)
        dc_val = int(block_scan[0])

        # DC size + bits
        dc_size = self.__magnitude_size(dc_val)      # How many bits needed to represent DC
        dc_bits = self.__magnitude_bits(dc_val, dc_size)  # Actual bitstring for DC

        # AC coefficients follow the DC
        ac = block_scan[1:]

        rle = []       # List of ((run, size), bits) tuples
        zero_run = 0   # Count consecutive zeros for run-length encoding

        for coeff in ac:
            coeff = int(coeff)

            if coeff == 0:
                zero_run += 1
                # JPEG: if 16 consecutive zeros, use ZRL (Zero Run Length)
                if zero_run == 16:
                    rle.append(((15, 0), ""))  # ZRL symbol
                    zero_run = 0
            else:
                size = self.__magnitude_size(coeff)         # Number of bits to represent AC coefficient
                bits = self.__magnitude_bits(coeff, size)  # Actual bits for this AC coefficient
                rle.append(((zero_run, size), bits))       # Store run-length + size as symbol, plus bits
                zero_run = 0  # Reset zero run

        # End of Block (EOB) if remaining coefficients are zero
        if zero_run > 0:
            rle.append(((0, 0), ""))  # EOB symbol

        # Return dictionary with DC and RLE AC values
        return {
            "DC": (dc_size, dc_bits),
            "AC": rle
        }

    def __magnitude_size(self, value):
        # Number of bits required to represent a value
        if value == 0:
            return 0
        return abs(value).bit_length()  # abs to handle negative numbers

    def __magnitude_bits(self, value, size):
        # Convert a value into its bitstring representation for JPEG
        if size == 0:
            return ""

        # Convert absolute value to binary string
        # --> pad to <size> bits with leading 0s!
        bits = format(abs(value), f"0{size}b")
        if value < 0:
            # JPEG negative representation: invert bits of magnitude
            bits = ''.join('1' if b=='0' else '0' for b in bits)
        return bits
