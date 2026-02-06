from collections import Counter
import heapq

class HuffmanEncoder:

    # Build a Huffman table for a list of symbols
    # --> Symbols can be AC or DC
    # --> return mapping of symbol to Huffman code (in a dictionary)
    # --> ENSURE no code exceeds 16 bits (JPEG-compliant)
    def __build_table(self, symbols):

        # Count how often each symbol appears
        # --> more frequent symbols will get shorter Huffman codes!
        freq = Counter(symbols)

        # Sort symbols by frequency ascending (least frequent first)
        # --> x[1] refers to the frequency, x[0] is the symbol
        sorted_symbols = sorted(freq.items(), key=lambda x: x[1])

        # Initialize code lengths: all start at 0
        code_lengths = {symbol: 0 for symbol, _ in sorted_symbols}

        # Build a  Huffman tree using heap
        # In the beginning, all codes are empty --> will be filled with 0/1
        heap = [[weight, [[symbol, ""]]] for symbol, weight in sorted_symbols]
        heapq.heapify(heap)

        # Repeatedly merge the two least frequent nodes
        # until only one tree remains
        while len(heap) > 1:
            # Pop two nodes with smallest frequency
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)

            # Prefix '0' to all codes in the left subtree
            for entry in lo[1]:
                entry[1] = '0' + entry[1]
                code_lengths[entry[0]] += 1

            # Prefix '1' to all codes in the right subtree
            for entry in hi[1]:
                entry[1] = '1' + entry[1]
                code_lengths[entry[0]] += 1

            # Push merged node back into the heap
            # Frequencies add up, symbol lists concatenate
            heapq.heappush(
                heap,
                [lo[0] + hi[0], lo[1] + hi[1]]
            )

        # Extract preliminary symbol -> code mapping
        # Heap now looks like this: [ total_frequency, [ [symbol, code], [symbol, code], ... ] ]
        # --> heap[0][1] contains [symbol, code] pairs
        # --> build dictionary from that!
        temp_table = {symbol: code for symbol, code in heap[0][1]}

        # --- ENFORCE JPEG MAX CODE LENGTH = 16 ---
        MAX_LEN = 16  # JPEG limit
        # Find symbols exceeding MAX_LEN
        over_len = {symbol: length for symbol, length in code_lengths.items() if length > MAX_LEN}

        if over_len:
            # Simple redistribution: move extra symbols to max length
            for symbol in over_len:
                # Truncate code to 16 bits (leftmost bits kept)
                temp_table[symbol] = temp_table[symbol][-MAX_LEN:]
                code_lengths[symbol] = MAX_LEN

        # Final table ready
        return temp_table


    # Construct the tables from the provided blocks
    def build_tables(self, blocks):
        dc_symbols = []
        ac_symbols = []

        for block in blocks:
            # DC: size only
            dc_size, _ = block['DC']
            dc_symbols.append(dc_size)

            # AC symbols
            for ac in block['AC']:
                #if ac == ('ZRL',) or ac == ('EOB',):
                #    ac_symbols.append(ac)
                if (ac == ('ZRL',)):
                    ac_symbols.append((15,0))
                elif(ac == ('EOB',)):
                    ac_symbols.append((0,0))
                else:
                    (run, size), _ = ac
                    ac_symbols.append((run, size))

        dc_table = self.__build_table(dc_symbols)
        ac_table = self.__build_table(ac_symbols)
        print(f"DC Table: {dc_table}")
        print(f"AC Table: {ac_table}")
        return { "DC": dc_table, "AC": ac_table }

    # Encode individual blocks  --> treat
    # AC and DC components separately -->
    # Now we need the encoded bits from the previously generated Huffman tables!
    def encode_bitstream(self, blocks, tables):
        bitstream = ""
        dc_table = tables['DC']
        ac_table = tables['AC']

        for block in blocks:
            size, bits = block['DC']
            bitstream += dc_table[size]
            bitstream += bits

            for ac in block['AC']:
                #if ac == ('ZRL',) or ac == ('EOB',):
                #    bitstream += ac_table[ac]
                if (ac == ('ZRL',)):
                    bitstream += ac_table[(15,0)]
                elif(ac == ('EOB',)):
                    bitstream += ac_table[(0,0)]
                else:
                    (run, size), bits = ac
                    bitstream += ac_table[(run, size)]
                    bitstream += bits

        print(f"Bitstream: {bitstream}")
        return bitstream

