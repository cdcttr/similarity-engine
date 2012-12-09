
A = load '$src' using PigStorage('\t') as (oid:long, title:chararray);

BEST = load '$keys' using PigStorage('\t') as (parent:long, child:long);

LP = GROUP BEST BY parent;
LPP = FOREACH LP GENERATE group as parent:long, group as child:long;
L = UNION BEST, LPP;

M = JOIN A by oid, L by child;

N = FOREACH M GENERATE L::parent, L::child, A::title;

O = ORDER N BY parent, child;

STORE O into '$dest';
