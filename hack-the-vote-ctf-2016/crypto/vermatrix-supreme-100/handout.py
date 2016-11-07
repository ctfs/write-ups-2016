import sys, random, time

flag = "flag{1_sw34r_1F_p30Pl3_4cTu4lLy_TrY_Th1s}"

def printmat(matrix):
	for row in matrix:
		for value in row:
			print value,
		print ""
	print ""


def pad(s):
	if len(s)%9 == 0:
		return s
	for i in xrange((9-(len(s)%9))):
		s.append(0)
	return s

def genBlockMatrix(s):
	outm = [[[7 for x in xrange(3)] for x in xrange(3)] for x in xrange(len(s)/9)]
	for matnum in xrange(0,len(s)/9):
		for y in xrange(0,3):
			for x in xrange(0,3):
				outm[matnum][y][x] = s[(matnum*9)+x+(y*3)]
	return outm


def fixmatrix(matrixa, matrixb):
	out = [[0 for x in xrange(3)] for x in xrange(3)]	
	for rn in xrange(3):
		for cn in xrange(3):
			out[cn][rn] = (int(matrixa[rn][cn])|int(matrixb[cn][rn]))&~(int(matrixa[rn][cn])&int(matrixb[cn][rn]))
	return out


def chall():
	IV = [c for c in '?????????']
	seed = "??????????????????"


	blocks = genBlockMatrix(pad(IV + [ord(c) for c in seed]))

	res = [[0 for i in xrange(3)] for i in xrange(3)]
	for i in xrange(len(blocks)):
		res = fixmatrix(res, blocks[i])


	print "SEED: " + str(seed)
	printmat(res)

	data = raw_input("")

	data = data.replace(' ', '').strip().split(',')

	if len(data) != 9:
		return False

	for i in xrange(len(IV)):
		if str(IV[i]) != str(data[i]):
			return False

	return True


if chall():
	print flag

