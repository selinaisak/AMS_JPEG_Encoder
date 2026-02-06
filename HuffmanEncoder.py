from collections import Counter
import heapq

class HuffmanEncoder:
    def __init__(self):
        # Store separate tables for DC/AC symbols
        self.dc_table = {}
        self.ac_table = {}

    # Build a Huffman table for a list of symbols
    # --> Symbols can be AC or DC
    # --> return mapping of symbol to Huffman code (in a dictionary)
    def __build_table(self, symbols):

        # Count how often each symbol appears
        # --> more frequent symbols will get shorter Huffman codes!
        freq = Counter(symbols)

        # Build an initial min-heap
        # Each entry looks like:
        #   [frequency, [[symbol, ""]]]
        # The empty string will be filled with '0'/'1' bits during tree construction
        heap = [[weight, [[symbol, ""]]] for symbol, weight in freq.items()]
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

            # Prefix '1' to all codes in the right subtree
            for entry in hi[1]:
                entry[1] = '1' + entry[1]

            # Push merged node back into the heap
            # Frequencies add up, symbol lists concatenate
            heapq.heappush(
                heap,
                [lo[0] + hi[0], lo[1] + hi[1]]
            )

        # Extract final symbol → code mapping
        # Heap now looks like this: [ total_frequency, [ [symbol, code], [symbol, code], ... ] ]
        # --> heap[0][1] contains [symbol, code] pairs
        # --> build dictionary from that!
        return {symbol: code for symbol, code in heap[0][1]}


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
                if ac == ('ZRL') or ac == ('EOB'):
                    ac_symbols.append(ac)
                else:
                    (run, size), _ = ac
                    ac_symbols.append((run, size))

        self.dc_table = self.__build_table(dc_symbols)
        self.ac_table = self.__build_table(ac_symbols)
        print(f"DC Table: {self.dc_table}")
        print(f"AC Table: {self.ac_table}")

    # Encode individual blocks  --> treat
    # AC and DC components separately -->
    # Now we need the encoded bits from the previously generated Huffman tables!
    def encode_bitstream(self, blocks):
        bitstream = ""

        for block in blocks:
            size, bits = block['DC']
            bitstream += self.dc_table[size]
            bitstream += bits

            for ac in block['AC']:
                if ac == ('ZRL') or ac == ('EOB'):
                    bitstream += self.ac_table[ac]
                else:
                    (run, size), bits = ac
                    bitstream += self.ac_table[(run, size)]
                    bitstream += bits

        print(f"Bitstream: {bitstream}")
        return bitstream

