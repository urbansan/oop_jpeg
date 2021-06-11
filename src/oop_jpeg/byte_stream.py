class ByteStream:
    def __init__(self, filename):
        self.position = 0
        self.bytes = []
        with open(filename, "rb") as f:
            while True:
                b = int(f.read(1).hex(), base=16)
                if not b:
                    break
                self.bytes.append(b)

    def next_byte(self):
        pos = self.position
        self.position += 1
        return self.bytes[pos]
