import math

class SymbolEncoder:

    # Convert coefficients into JPEG entropy symbols and magnitude bits.
    # --> Prepare for Huffman encoding!

    # Output:
    # - DC: (SIZE, bitstring)
    # - AC: [((RUN, SIZE), bitstring), ..., EOB / ZRL]


    def encode(self, Y_rle, Cb_rle, Cr_rle):
        return (
            self.__encode_channel(Y_rle),
            self.__encode_channel(Cb_rle),
            self.__encode_channel(Cr_rle)
        )

    def __encode_channel(self, channel_blocks):
        # Encode all blocks of one channel first
        encoded_blocks = []
        for block in channel_blocks:
            encoded_blocks.append(self.__encode_block(block))
        return encoded_blocks

    def __encode_block(self, block):
        # Encode a single block
        #
        # For DC:
        #   - Calculate SIZE
        #   - Calculate bits
        #
        # For AC:
        #   - Convert(RUN, VALUE) pairs into: (RUN, SIZE) symbols + bits

        # DC coefficient
        dc_value = block["DC"]
        dc_size, dc_bits = self.__encode_value(dc_value)
        # The bit length MUST be equivalent to size!
        assert len(dc_bits) == dc_size or dc_size == 0

        # AC coefficients
        ac_encoded = []

        for run, value in block["AC"]:

            # End Of Block symbol (all remaining ACs are zero)
            if (run, value) == (0, 0):
                ac_encoded.append(("EOB"))
                continue

            # Zero Run Length symbol (16 consecutive zeros)
            if (run, value) == (15, 0):
                ac_encoded.append(("ZRL"))
                continue

            # Normal AC coefficient
            # Convert VALUE into SIZE and bits
            size, bits = self.__encode_value(value)
            # The bit length MUST be equivalent to size!
            assert len(bits) == size or size == 0
            ac_encoded.append(((run, size), bits))

        return {
            "DC": (dc_size, dc_bits),
            "AC": ac_encoded
        }

    def __encode_value(self, value):
        # Encode value (integer) into:
        #   - SIZE
        #   - bits
        # Positive values: normal binary
        # Negative values: inverted binary

        # Zero is a special case
        if value == 0:
            return 0, ""

        abs_value = abs(value)

        # Use log2 to get the necessary bits --> + 1,
        # because even log2(1) = 0 --> still needs a bit!
        size = int(math.floor(math.log2(abs_value)) + 1)

        # Convert absolute value to binary string
        # --> pad to <size> bits with leading 0s!
        bits = format(abs_value, f"0{size}b")

        # JPEG negative number encoding:
        # invert all bits of the positive representation
        if value < 0:
            bits = ''.join('1' if b == '0' else '0' for b in bits)
            # Check the negative value too!
            # The bit length MUST be equivalent to size!
            # Size CANNOT be 0, as negative numbers need at least 1 bit!
            assert len(bits) == size

        return size, bits
