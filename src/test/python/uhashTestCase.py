import unittest
import uhash

class uhashTestCase(unittest.TestCase):
	def test_vectoruhash(self):
		uh = uhash.VectorUHash(0x123456)
		print uh.hashbytes("hello")
		print uh.hashbytes("hellow")
		print uh.hashbytes("d")
		print uh.hashbytes("e")
		print uh.hashbytes("ee")
		print uh.hashbytes("hello")

	def test_vectoruhash2(self):
		uh = uhash.VectorUHash(0x123456)
		self.assertTrue(uh.hashbytes("d") != uh.hashbytes("e"))

	def test_uhash(self):
		uh = uhash.UHash(50)
		hashes = uh.hash("t")
		for h in hashes:
			count = 0
			for y in hashes:
				if h == y:
					count += 1
			self.assertTrue(count == 1)
		print hashes

	def test_uhash_equality(self):
		uh = uhash.UHash(50)
		h1 = uh.hash("test")
		h2 = uh.hash("test2")
		h3 = uh.hash("test")

		for x, y in zip(h1, h2):
			# note: this may not always be true
			self.assertTrue(x != y)

		for x, y in zip(h1, h3):
			# note: this is always true
			self.assertTrue(x == y)




if __name__ == '__main__':
    unittest.main()
