class ByteStream:
    def __init__(self, filename):
        self.position = 0
        self.bytes = []
        with open(filename, "rb") as f:
            while True:
                b = f.read(1)
                if b == b"":
                    break
                b = int(b.hex(), base=16)
                self.bytes.append(b)

    def next_byte(self):
        pos = self.position
        self.position += 1
        # b = hex(self.bytes[pos])
        return self.bytes[pos]

    def next_bytes(self, amount: int):
        return [self.next_byte() for _ in range(amount)]

    def __bool__(self):
        return self.position < len(self.bytes)
