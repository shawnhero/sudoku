Sudoku Solution
---
Written by wuxu@cs.ucla.edu


#Usage
`python sudoku.py [filename] [optional: output_filename]`


#Concepts


- Square `A single element of the sudoku.`
- Units  `row, col, and 3*3 it belongs to. Should be a list of a list of peer squares`
- Peers `A list of all the related elements`

See reference: http://norvig.com/sudoku.html for a detailed explanation of the concepts.

#Improvements
The key algorithm is inspired from the reference. However, there's one improvement based on the search-based constraint propagation.

Here is a simple solution to choose the next key to search. It chooses the one with least number of possible choices.

```
def nextKey(self, su):
    # the commented line below offers a naive solution, which works well
    return min(su, key=lambda x: len(su[x]) if len(su[x])!=1 else 10)
```


Here is the improved part. Basically it tries to avoid the peers of the previously searched keys.
```
def nextKey(self, su):
    # it turns out the way below works slightly better
    preKeys = self.searched
    keylist = [(len(su[key]), key) for key in self.squares if len(su[key]) > 1]
    if not keylist:
        # all len equal 1, solved
        return False
    minnum0, next0 = min(keylist)
    if not preKeys:
        # c0 stores all the positions that are not the peer of the searched keys
        c0 = set(self.squares) - set(sum([list(peers[pkey]) for pkey in preKeys],[]))
        clist = [(len(su[key]), key) for key in c0 if len(su[key]) > 1]
        if not clist:
            # either c0 empty or all solved in c0
            return next0
        minnum1, next1 = min(clist)
        if(minnum0==minnum1):
            return next1
    return next0
```

Using the test cases attached as a comparision:

    input.csv, simple
        Time Used, 0.0021
        Num of searches, 6

    input.csv, improved
        Time Used, 0.0022
        Num of searches, 4

    hard.csv, simple
        Time Used, 0.0118
        Num of searches, 38

    hard.csv, improved
        Time Used, 0.0136
        Num of searches, 22


    hardest.csv, simple
        Time Used, 0.0531
        Num of searches, 197

    hardest.csv, improved
        Time Used, 0.059
        Num of searches, 102

