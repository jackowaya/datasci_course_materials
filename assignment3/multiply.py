import MapReduce
import sys
from collections import defaultdict

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

# Possibly cheating here
MATRIX_SIZE = 5 # square

def mapper(record):
    # record is matrix, i, j, value
    # output (output spot), record
    # Can't do output location without knowing the full matrix size...
    if record[0] == 'a':
        # Map to same row
        for i in range(MATRIX_SIZE):
            mr.emit_intermediate((record[1], i), record)
    else:
        # Map to column
        for i in range(MATRIX_SIZE):
            mr.emit_intermediate((i, record[2]), record)

def reducer(key, list_of_values):
    # key: location
    # value: list of records
    arecs = defaultdict(int)
    brecs = defaultdict(int)
    for record in list_of_values:
        if record[0] == 'a':
            arecs[record[2]] = record[3]
        else:
            brecs[record[1]] = record[3]
    
    total = 0
    for index in arecs.keys():
        total += arecs[index] * brecs[index]

    mr.emit((key[0], key[1], total))
    
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
