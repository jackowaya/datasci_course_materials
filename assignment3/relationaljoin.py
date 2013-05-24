import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: record source
    # value: tuple
    mr.emit_intermediate(record[1], record)

def reducer(key, list_of_values):
    # key: order id
    # value: record source, value tuple
    for val in list_of_values:
        if val[0] == 'order':
            order_list = val
    if order_list is not None:
        for val in list_of_values:
            if val[0] == 'line_item':
                output = list(order_list)
                output.extend(val)
                mr.emit(output)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
