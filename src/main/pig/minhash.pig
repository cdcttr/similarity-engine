-- uhash.pig
register 'src/main/python/minhash.py' using jython as minhash;

AL = load '$src' using PigStorage('\t') as (oid:long, title:chararray);

A = ORDER AL BY oid;

B = FOREACH A GENERATE oid, FLATTEN(TOKENIZE(title)) as word;

C = FOREACH B GENERATE oid, word, minhash.uhash(LOWER(word));

D = GROUP C BY oid;

EP = FOREACH D GENERATE group as oid:long, minhash.minhash(C) as mh;

STORE EP INTO '$destminhash';

E = FOREACH EP GENERATE minhash.joinkey(mh.h1, mh.h2) as jk1:int, minhash.joinkey(mh.h5, mh.h9) as jk2:int,
						minhash.joinkey(mh.h3, mh.h4) as jk3:int, minhash.joinkey(mh.h10, mh.h11) as jk4:int, oid, mh;

F = GROUP E BY jk1;
G = GROUP E BY jk2;
--F3 = GROUP E BY jk3;
--F4 = GROUP E BY jk4;

H1 = FOREACH F GENERATE group as jk, FLATTEN(E.(oid,mh)) as (oid, mh), COUNT(E) as c;
H2 = FOREACH G GENERATE group as jk, FLATTEN(E.(oid,mh)) as (oid, mh), COUNT(E) as c;
--H3 = FOREACH F3 GENERATE group as jk, FLATTEN(E.(oid,mh)) as (oid, mh), COUNT(E) as c;
--H4 = FOREACH F4 GENERATE group as jk, FLATTEN(E.(oid,mh)) as (oid, mh), COUNT(E) as c;

-- only join items that belong in groups > 1
HC1 = FILTER H1 BY c > 1;
HC2 = FILTER H2 BY c > 1;
--HC3 = FILTER H3 BY c > 1;
--HC4 = FILTER H4 BY c > 1;

I = UNION HC1, HC2;--, HC3, HC4;

J1 = ORDER I BY jk;
J2 = FOREACH J1 GENERATE *;

--STORE J1 into 'join-keys';

-- create each candidate pair by joining
JP = JOIN J1 by jk, J2 by jk;
-- score each candidate pair
K = FOREACH JP GENERATE J1::oid as parent:long, J2::oid as child:long, minhash.overlap(J1::mh, J2::mh) as jaccard:int;
-- filter cnadidate pairs by threshold
LL = FILTER K by jaccard > $minjaccard; 

LM = FILTER LL BY parent > child;
LN = FILTER LL BY parent < child;

LS = FOREACH LM GENERATE child as parent:long, parent as child:long, jaccard;
LZ = UNION LS, LN;

GBP = GROUP LZ BY child;
BEST = FOREACH GBP {
	s = ORDER LZ BY jaccard;
	t = LIMIT s 1;
	GENERATE FLATTEN(t);
};

STORE BEST INTO '$dest';

