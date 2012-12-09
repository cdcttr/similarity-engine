#!/usr/bin/python
import sys
from org.apache.pig.scripting import Pig
from bidipig import runbidi

# make minhash clusters
minhash = Pig.compileFromFile('src/main/pig/minhash.pig')

osrc = src = sys.argv[1]
destminhash = sys.argv[2] + '-minhash'
dest = sys.argv[2] + '-jaccard'
minjaccard = 80

bound = minhash.bind()

job = bound.runSingle()

if not job.isSuccessful():
	raise 'failed in minhash'
# output is pairs and scores

# make transitive closure of clusters
src = dest
dest = sys.argv[2] + '-bidi'
runbidi(src, dest)

# join with original data
join = Pig.compileFromFile('src/main/pig/join.pig')

src = osrc
keys = dest
dest = sys.argv[2]

bound = join.bind()

job = bound.runSingle()

if not job.isSuccessful():
	raise 'failed in join'

