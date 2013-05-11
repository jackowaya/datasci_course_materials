select sum(aval*bval) from (
select a.value as aval, b.value as bval from a, b where a.row_num = 2 and b.col_num = 3 and a.col_num = b.row_num
);