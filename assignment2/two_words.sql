select count(*) from 
(
select distinct(docid) as d from frequency where (select count(*) from frequency where term = 'transactions' and docid = d) and (select count(*) from frequency where term='world' and docid=d)
);

