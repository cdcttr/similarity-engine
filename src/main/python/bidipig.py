#!/usr/bin/python
import sys
from org.apache.pig.scripting import Pig 

def runbidi(src, fdest):
	P = Pig.compileFromFile('src/main/pig/bidi.pig')

	cntsbase = 'counts'
	Pig.fs('rmr ' + cntsbase)

	for count in range(10):
		dest = fdest + 'gm%04d' % count
		Pig.fs('rmr ' + dest)
		cnts = cntsbase
		params = {'src':src, 'dest':dest, 'cnts':cnts}
		bound = P.bind(params)
		job = bound.runSingle()

		if not job.isSuccessful():
			raise 'failed'

		src = dest

		iter = job.result('S').iterator()
		if iter.hasNext():
			Pig.fs('rmr ' + cnts)
		else:
			Pig.fs('mv ' + dest + ' ' + fdest)
			print 'ALL DONE!'
			break


if __name__ == "__main__":
	src = sys.argv[1]
	dest = sys.argv[2]
	runbidi(src, dest)
