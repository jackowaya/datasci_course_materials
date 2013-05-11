select max(score) from
(
select doc1, doc2, sum(termscore) as score from 
(select d1.docid as doc1, d2.docid as doc2, d1.count * d2.count as termscore from 
(
SELECT 'q' as docid, 'washington' as term, 1 as count 
UNION
SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION 
SELECT 'q' as docid, 'treasury' as term, 1 as count
) d1, frequency d2 where d1.term = d2.term)
group by doc1, doc2
);

