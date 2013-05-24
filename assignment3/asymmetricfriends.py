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
    if key < value:
        mr.emit_intermediate((key, value), record)
    else:
        mr.emit_intermediate((value, key), record)

def reducer(key, list_of_values):
    # key: sorted persona personb tuple
    # value: list of observed persona personb tuples
    if len(list_of_values) == 1:
        mr.emit(key)
        mr.emit((key[1], key[0]))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
