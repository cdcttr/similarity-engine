#!/usr/bin/python
from org.apache.pig.scripting import Pig
from org.apache.pig.impl.logicalLayer.schema import Schema
from org.apache.pig.data import DataType
import struct
import uhash
from uhash import VectorUHash;
"""
Pig UDFs for Locality Sensitive Hashing using min-hashing

Shows different methods of exposing Python UDF schemas
"""

SIZE = 20
uh = uhash.UHash(SIZE)

@outputSchemaFunction("uhashschema")
def uhash(token):
	return tuple(uh.hash(token))

@schemaFunction("uhashschema")
def uhashschema(input):
	s = Schema()
	for i in xrange(SIZE):
		s.add(Schema.FieldSchema('h%d' % i, DataType.INTEGER))

	return s

@outputSchemaFunction("uhashschema")
def minhash(bag):
	oid, word, mh = bag[0]
	minhash = list(mh)
	for oid, word, hashes in bag:
		for pos, values in enumerate(zip(minhash, hashes)):
			i, j = values
			minhash[pos] = min(i,j)

	return tuple([int(x & 0x7fffffff) for x in minhash])


@outputSchema("jaccard:int")
def overlap(t1, t2):
	t = 0
	o = 0
	for i, j in zip(t1, t2):
		if i == j:
			o += 1
		t += 1
	return (o*100)/t

# For join key UDF
vh = VectorUHash(0x12345)

@outputSchema("jk:int")
def joinkey(v1, v2):
	return int(vh.hashbytes(struct.pack('II', v1, v2)) & 0x7fffffff)
