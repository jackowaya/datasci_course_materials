select count(*) from 
(select docid, sum(count) as total from frequency group by docid having total > 300);

