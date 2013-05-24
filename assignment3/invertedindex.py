import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    words_seen = set()
    for w in words:
      if w not in words_seen:
          mr.emit_intermediate(w, key)
          words_seen.add(w)

def reducer(key, list_of_values):
    # key: word
    # value: list of docids
    mr.emit((key, list_of_values))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
