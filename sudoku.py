# Written by wuxu@cs.ucla.edu
# Reference: http://norvig.com/sudoku.html
# Key algorithm is inspired from the reference, with code rewrote and refined

import csv
import sys

import timeit


def cross(A, B):
		return [a+b for a in A for b in B]

class Sudoku():
	sudoku = None
	rows = 'ABCDEFGHI'
	cols = '123456789'
	squares = cross(rows, cols)
	rowlist = [cross(row, cols) for row in rows]
	collist = [cross(rows, col) for col in cols]
	sublist = [cross(r, c) for r in ['ABC', 'DEF', 'GHI'] for c in ['123', '456', '789']]
	unitlist = rowlist + collist + sublist
	## units: dict; key: some square; val: unitlist it belongs to
	units = None
	## peers: dict; key: some square; val: a set of peers
	peers = None

	count = 0

	def __init__(self, filename=None):
		# given a filename, initialize the sudoku
		# replace 0 with 123456789
		self.units = dict([key, [r for r in self.unitlist if key in r]] for key in self.squares)
		self.peers = dict([key, set(sum(self.units[key],[]))-set([key])] for key in self.squares)
		try:
			csvfile = open(filename,'r')
			myfile = csv.reader(csvfile)
			raw = [row for row in myfile]
			lenraw = [len(row)!=9 for row in raw]
			# check the format of file
			if any(lenraw) or len(lenraw)!=9:
				print "Bad Formatted File!"
				sys.exit(0)
			self.sudoku = dict([key, raw[ord(key[0])-ord('A')][int(key[1])-1] ] for key in self.squares)
			print "File Loaded:"
			self.display(self.sudoku)
			self.sudoku = dict([key, self.convert(raw[ord(key[0])-ord('A')][int(key[1])-1])] for key in self.squares)
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			sys.exit(0)
		except:
			print "Unexpected error:", sys.exc_info()[0]
			sys.exit(0)

	def convert(self, str):
		return str if str!='0' else '123456789'


	def clean(self):
		# first we clean the sudoku by narrowing each unknown fields
		for key in self.sudoku:
			if self.sudoku[key] == '123456789':
				for d in self.peers[key]:
					if len(self.sudoku[d])==1:
						self.sudoku[key] = self.sudoku[key].replace(self.sudoku[d], '')


	def display(self, values):
		#Display these values as a 2-D grid.
		width = 1+max(len(values[s]) for s in self.squares)
		line = '+'.join(['-'*(width*3)]*3)
		for r in self.rows:
			print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
						  for c in self.cols)
			if r in 'CF': print line

	#assign sudoku[key] to be d
	def assign(self, su, key, d):
		##print "Assigning ", key, " with value", d
		# assgining is equal to eliminate all the others one by one
		allother = su[key].replace(d,'')
		##print allother
		if all(self.eliminate(su, key, other) for other in allother):
			return su
		return False
		
			   
	## do a elimination of d from sudoku[key]
	def eliminate(self, su, key, d):
		##print "Eliminating ", d, 'from ', su[key]
		if d not in su[key]:
			# already elminated
			return su
		su[key] = su[key].replace(d, '')
		##print "Now it becomes", su[key]
		val = su[key]
		if len(val)==0:
			##print 'Cannot Eliminate the only value'
			return False
		if len(val)==1:
			# eliminate all the peers
			if not all(self.eliminate(su, p, val) for p in self.peers[key]):
				return False
		# now we check all the units if some square becomes certain
		for u in self.units[key]:
			places = [e for e in u if d in su[e]]
			if len(places)==0:
				##print "Conflict in this unit! No place for ", d
				return False
			if len(places)==1:
				##print "Only one place for ", d, "Assigning.."
				return self.assign(su, places[0], d)
		return su

	def minLenKey(self,s):
		# return the next search point of sudoku s
		# it will be the one with minumum choices
		return min(s, key=lambda x: len(s[x]) if len(s[x])!=1 else 10)
		
	def solve(self):
		self.count = 0
		# solve the problem
		# give the initial search point
		self.sudoku =  self.search(self.sudoku, self.minLenKey(self.sudoku))
		return self.sudoku

	def search(self,values, skey, level=0):
		self.count += 1
		if(len(values[self.minLenKey(values)])==1):
			## solved! search end
			return values
		deads = 0
		for i in values[skey]:
			assigned = self.assign(values.copy(), skey, i)
			if assigned:
				# continue search
				result = self.search(assigned, self.minLenKey(assigned), level+1)
				if result:
					return result
				else:
					deads +=1
			else:
				deads +=1
		if deads==len(values[skey]):
			return False

	def save(self, filename="solution.csv"):
		# save the result
		try:
			csvfile = open(filename, 'w')
			mywriter = csv.writer(csvfile)
			table = [[self.sudoku[r] for r in cross(r,self.cols)] for r in self.rows]
			mywriter.writerows(table)
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
		except:
			print "Unexpected error:", sys.exc_info()[0]
			
def test():
	# calculate the time used
	start = timeit.default_timer()

	if len(sys.argv)<2:
		print "Usage: python sudoku [filename]"
		sys.exit(0)		
	if sys.argv[1]:
		filename = sys.argv[1]
	if len(sys.argv)>2 and sys.argv[2]:
		output = sys.argv[2]
	else:
		output = "solution.csv"
	sudoku = Sudoku(filename)
	sudoku.clean()
	print "\nSolution:"
	sudoku.display(sudoku.solve())
	sudoku.save(output)
	print "Solution saved as", output

	stop = timeit.default_timer()
	print "Time Used,", round(stop - start, 4)
	print "Num of searches,", sudoku.count


if __name__ == "__main__":
	test()