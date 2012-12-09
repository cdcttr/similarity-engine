
import java.util.Random as Random
import struct

"""
UHash - more acurately it is a Vector of Hashes
"""
class UHash:
	def __init__(self, count, seed=0x123322):
		random = Random(seed)
		self.count = count
		self.hashers = [VectorUHash(random.nextLong()) for i in xrange(count)]

	def hash(self, b):
		return [h.hashbytes(b) for h in self.hashers]


class VectorUHash:
	def __init__(self, seed):
		self.random = Random(seed)
		self.seed = seed

	def __hash(self, b):
		self.random.setSeed(self.seed)

		p = 0
		sum = 0

		while p < len(b):
			c = 0
			d = [0,0,0,0]
			while p < len(b) and c < 4:
				d[c] = ord(b[p])
				c += 1
				p += 1

			x1 = (int(d[0]) & 0xff) + ((int(d[1]) & 0xff) << 8) +\
					((int(d[2]) & 0xff) << 16) + ((int(d[3]) & 0xff) << 24)

			c = 0
			e = [0,0,0,0]
			while p < len(b) and c < 4:
				e[c] = ord(b[p])
				c += 1
				p += 1

			x2 = (int(e[0]) & 0xff) + ((int(e[1]) & 0xff) << 8) +\
					((int(e[2]) & 0xff) << 16) + ((int(e[3]) & 0xff) << 24)

			a1 = self.random.nextLong()
			a2 = self.random.nextLong()

			a1 |= 1
			a2 |= 1

			x1 += a1
			x2 += a2

			if x2 != 0:
				x1 *= x2
			sum += x1
		return int(sum & 0x7fffffff)

	def hashbytes(self, bytes):
		return self.__hash(bytes)


