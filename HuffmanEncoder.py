class HuffmanEncoder:
    def __init__(self):
        # Store separate tables for DC/AC symbols
        self.dc_table = {}
        self.ac_table = {}