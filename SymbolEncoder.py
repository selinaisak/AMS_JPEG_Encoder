class SymbolEncoder:

    # IMPORTANT:
    # At this stage, coefficients are ALREADY encoded into:
    # - DC: (SIZE, bitstring)
    # - AC: [((RUN, SIZE), bitstring), ..., (0,0)=EOB, (15,0)=ZRL]
    #
    # Therefore: NO magnitude calculation is done here anymore!

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
        # DC:
        #   - Already encoded as (SIZE, bits)
        #
        # AC:
        #   - Already encoded as ((RUN, SIZE), bits)
        #   - ZRL  = ((15, 0), "")
        #   - EOB  = ((0, 0), "")

        # DC coefficient (already encoded)
        dc_size, dc_bits = block["DC"]

        # AC coefficients (already encoded)
        ac_encoded = []

        for ac in block["AC"]:
            # AC entries are already in final JPEG symbol form
            ac_encoded.append(ac)

        return {
            "DC": (dc_size, dc_bits),
            "AC": ac_encoded
        }
