import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: personA
    # value: personB
    key = record[0]
    value = record[1]
    mr.emit_intermediate(record[0], 1)

def reducer(key, list_of_values):
    # key: person id
    # value: list of 1s for each friend
    mr.emit((key, len(list_of_values)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
