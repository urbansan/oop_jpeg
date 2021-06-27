from typing import Iterable
from functools import reduce


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


class BitStream:
    def __init__(self, bytes_: Iterable):
        self.byte_position = -1
        self.bit_position_generator = self._bit_position_generator(7)
        self.bytes = list(bytes_)
        # self.bit_gen = self.next_bit()

    def next_bit(self):
        bit_position = next(self.bit_position_generator)
        if bit_position == 7:
            self.byte_position += 1
        try:
            bit = self.bytes[self.byte_position] >> bit_position & 1
        except IndexError as er:
            raise EOFError("Bit stream has finished") from er
        return bit

    def next_bits(self, length):
        bits = [self.next_bit() for _ in range(length)]
        return self._merge_bits(bits)

    @staticmethod
    def _merge_bits(bits: Iterable[int]):
        return reduce(lambda x, y: x << 1 | y, bits)

    @staticmethod
    def _bit_position_generator(n=7):
        while True:
            yield n
            n -= 1
            n = 7 if n < 0 else n


if __name__ == "__main__":

    b = BitStream([0xFA, 0xBA])
    # for bit in b.yield_bits():
    #     print(bit)
    a = b.next_bits(8)
    print(bin(a))
    c = b.next_bits(8)
    print(bin(c))