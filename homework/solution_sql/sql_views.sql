-- query_a
drop view query_a;
create view query_a as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status 
from student s, transcript t 
where s.ssn = t.ssn
and t.dcode = 'CS'
and t.cno = 530
order by s.ssn;

-- query_b
drop view query_b;
create view query_b as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status 
from student s, transcript t 
where s.ssn = t.ssn
and t.dcode = 'CS'
and t.cno = 530
and s.name = 'John'
order by s.ssn;

-- query_c
drop view query_c;
create view query_c as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status 
from student s
where not exists (
    select 1 from prereq p
    where not exists ( 
        select 1 from enrollment e, class c
        where e.class = c.class
        and c.dcode = p.dcode
        and c.cno = p.cno
        and exists (
            select 1 from transcript t
            where t.ssn = s.ssn
            and t.dcode = p.pcode
            and t.cno = p.pno
            and grade in ('A', 'B'))
        )
)
order by s.ssn;


-- query_d
drop view query_d;
create view query_d as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status 
from student s
where s.ssn in (
    select ssn from (
        select e.ssn, c.dcode, c.cno from enrollment e, class c
        where e.class = c.class 
        
        minus 
        
        select e.ssn, c.dcode, c.cno from enrollment e, class c
        where e.class = c.class
        and (
            not exists (
                select 1 from prereq p
                where c.dcode = p.dcode
                and c.cno = p.cno
            )
            or (
            exists (
                select 1 from prereq p, transcript t
                where c.dcode = p.dcode
                and c.cno = p.cno
                and t.dcode = p.pcode
                and t.cno = p.pno
                )
            and 
            not exists (
                select 1 from prereq p, transcript t
                where c.dcode = p.dcode
                and c.cno = p.cno
                and t.dcode = p.pcode
                and t.cno = p.pno
                and grade in ('C', 'F')
            )
        ))
    )
)
order by s.ssn;

-- query_e
drop view query_e;
create view query_e as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status
from student s
where s.name = 'John'
and s.ssn in (
    select ssn from (
        select e.ssn, c.dcode, c.cno from enrollment e, class c
        where e.class = c.class 
        
        minus 
        
        select e.ssn, c.dcode, c.cno from enrollment e, class c
        where e.class = c.class
        and (
            not exists (
                select 1 from prereq p
                where c.dcode = p.dcode
                and c.cno = p.cno
            )
            or (
            exists (
                select 1 from prereq p, transcript t
                where c.dcode = p.dcode
                and c.cno = p.cno
                and t.dcode = p.pcode
                and t.cno = p.pno
                )
            and 
            not exists (
                select 1 from prereq p, transcript t
                where c.dcode = p.dcode
                and c.cno = p.cno
                and t.dcode = p.pcode
                and t.cno = p.pno
                and grade in ('C', 'F')
            )
        ))
    )
)
order by s.ssn;

-- query_f
drop view query_f;
create view query_f as
select distinct c.dcode, c.cno from course c
where not exists (
    select 1 from prereq p
    where c.dcode = p.dcode
    and c.cno = p.cno)
order by c.dcode, c.cno;

-- query_g
drop view query_g;
create view query_g as
select distinct c.dcode, c.cno from course c
where exists (
    select 1 from prereq p
    where c.dcode = p.dcode
    and c.cno = p.cno)
order by c.dcode, c.cno;

-- query_h
drop view query_h;
create view query_h as
select distinct c.* from class c
where exists (
    select 1 from prereq p
    where c.dcode = p.dcode
    and c.cno = p.cno)
order by c.class;

-- query_i
drop view query_i;
create view query_i as
select distinct s.* from student s
    where s.ssn in (
    select distinct s.ssn from student s
    minus 
    select distinct s.ssn from student s
    where exists (
        select 1 from transcript t
        where s.ssn = t.ssn
        and t.grade in ('C', 'F'))
        )
order by s.ssn;

-- query_j
drop view query_j;
create view query_j as
select s.* 
from student s, enrollment e, class c, faculty f 
where f.name = 'Brodsky'
and s.ssn = e.ssn 
and e.class = c.class 
and c.instr = f.ssn
order by s.ssn;

-- query_k
drop view query_k;
create view query_k as
select distinct(e.ssn)
from enrollment e
where e.ssn in (
    select s.ssn
    from student s
    where not exists (
        select 1
        from class c
        where not exists (
            select 1
            from enrollment e
            where e.class = c.class
            and e.ssn = s.ssn
            )
        )
    )
order by e.ssn;

drop view query_l;
create view query_l as
select distinct(e.ssn)
from enrollment e
where e.ssn in (
    select s.ssn
    from student s
    where s.major = 'CS'
    and not exists (
        select 1
        from class c
        where dcode = 'MTH'
        and not exists (
            select 1
            from enrollment e
            where e.class = c.class
            and e.ssn = s.ssn
            )
        )
    )
order by e.ssn;
