-- load the file and bi-directionalize
A = LOAD '$src' using PigStorage('\t') as (parent:long, child:long);
B = FOREACH A GENERATE child as parent:long, parent as child:long;
C = UNION A, B;

-- work in groups
D = GROUP C BY parent;
-- for each parent group calculated the smallest child id
E = FOREACH D GENERATE group as g:long, FLATTEN(C) as (p:long,c:long), MIN(C.child) as m:long;
-- make two groups: one where the parent is larger than the smallest child
F = FILTER E BY g > m;
-- and another group where the parent is smaller than the smallest child
G = FILTER E BY g <= m;

-- where the parent is larger associate each child with the smallest child (the new parent)
H = FOREACH F GENERATE m as parent:long, c as child:long;
-- also remember to associate the old parent with the smallest child
HP= FOREACH F GENERATE m as parent:long, g as child:long;
-- output these as usual no relationship changes
I = FOREACH G GENERATE g as parent:long, c as child:long;

-- bring everyone together
J = UNION H, HP, I;
-- filter out node that point the themselves
JNE = FILTER J BY parent != child;

JPP = DISTINCT JNE;
-- store the answer for this round
STORE JPP INTO '$dest';

-- check if we are done
-- we are done if bi-directionalizing and reordering the parent child
-- created duplicates of each node
T = FOREACH JNE GENERATE *;
GRPS = GROUP T BY (parent, child);
CGRPS = FOREACH GRPS GENERATE FLATTEN(group), COUNT(T) as c:long;
V = ORDER CGRPS BY c;
S = FILTER CGRPS BY c < 2;
-- python code will check if this is empty - if it is, we are done
STORE S INTO '$cnts';
