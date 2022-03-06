import sys
sys.path.append('..')

import lib.rel_algebra_calculus.rel_algebra_calculus as ra
# note: you can use ra.imply(a,b) which expresses a --> b (a implies b)

def ha2(univDB):
    tables = univDB["tables"]
    department = tables["department"]
    course = tables["course"]
    prereq = tables["prereq"]
    # class may be a reserved word - check
    class_ = tables["class"]
    faculty = tables["faculty"]
    student = tables["student"]
    enrollment = tables["enrollment"]
    transcript = tables["transcript"]

    # ---------------------------------------------------------------
    # Your set creater functions or other helper functions (if needed)


    def student_transcript(s, transcript=transcript):
        return [{'dcode':t['dcode'], 'cno':t['cno'], 'grade':t['grade']} for t in transcript
                    if t['ssn'] == s['ssn']]

    # ---------------------------------------------------------------
    # Your queries

    #[OK] query_a
    query_a = [
        {"ssn": S["ssn"], "name":S["name"], "major":S["major"], "status":S["status"]}
        for S in student
            for T in transcript
                if S['ssn'] == T['ssn']
                if T['dcode'] == "CS"
                if T['cno'] == 530
    ]

    #[OK] query_b
    query_b = [
        {"ssn": S["ssn"], "name":S["name"], "major":S["major"], "status":S["status"]}
        for S in student
            for T in transcript
                if S['ssn'] == T['ssn']
                if S["name"] == "John"
                if T['dcode'] == "CS"
                if T['cno'] == 530
    ]


    # query_c


    def enrollment_class(s, enrollment=enrollment):
        return [{'dcode':e['dcode'], 'cno':e['cno']} 
                for e in enrollment 
                    for c in class_
                        if s['ssn'] == e['ssn']
                        if e['class'] == c['class']
    ]



    def student_transcript_pass(s):
        return [{'pcode':t['dcode'], 'pno':t['cno']}
            for t in transcript
                if s['ssn'] == t['ssn']
        
        ]

    query_c = ra.distinct([ {'ssn': s['ssn'], 'name': s['name'], 'major': s['major'], 'status': s['status']}
        for s in student
    ])

    # query_d
    query_d = ra.distinct([ {"tbd": "tbd"} ])

    # query_e
    query_e = ra.distinct([ {"tbd": "tbd"} ])

    #[OK] query_f
    
    def course_clean(s, course = course):
        return [{'dcode':c['dcode'], 'cno':c['cno']}
            for c in course
                if s['dcode'] == c['dcode']
                if s['cno'] == c['cno']
        ]

    def course_prereq(C, prereq = prereq):
        return [{'dcode':p['dcode'], 'cno':p['cno']}
                for p in prereq
    ]

    query_f = [
        {'dcode':C['dcode'], 'cno':C['cno']}
        for C in course
            for X in course_clean(C)
                if X not in course_prereq(C)
    ]

    #[OK] query_g
    query_g = ra.distinct([
        {'dcode':C['dcode'], 'cno':C['cno']}
        for C in course
            for P in prereq
                if C['dcode'] == P['dcode']
                if C['cno'] == P['cno']
    ]) 

    #[OK] query_h
    query_h = ra.distinct([
        {'class':Cls['class'], 'dcode':Cls['dcode'], 'cno':Cls['cno'], 'instr':Cls['instr']}
        for Cls in class_
            for P in prereq
                for C in course
                    if C['dcode'] == P['dcode']
                    if C['cno'] == P['cno']
                    if C['dcode'] == Cls['dcode']
                    if C['cno'] == Cls['cno']          
    ])

    # query_i

    def student_trans_grade(s):
        return [{'grade':t['grade']}
            for t in transcript
            if t['ssn'] == s['ssn']
        ]


    query_i = ra.distinct( [ {'ssn': s['ssn'], 'name': s['name'], 'major': s['major'], 'status': s['status']}

        for t in transcript
        for s in student
        if t['ssn'] == s['ssn']
        if all([ g in ['A', 'B'] 
                for g in student_trans_grade(s)
        ])
    ])

    #[OK] query_j
    query_j = [
        {"ssn": S["ssn"], "name":S["name"], "major":S["major"], "status":S["status"]}
        for S in student
            for E in enrollment
                for C in class_
                    for F in faculty
                        if S['ssn'] == E['ssn']
                        if E['class'] == C['class']
                        if C['instr'] == F['ssn']
                        if F['name'] == 'Brodsky'
    ]

    #[OK] query_k

    def student_enrollment(s, enrollment=enrollment, class_=class_):
        return [{'dcode':c['dcode'], 'cno':c['cno'], 'class':c['class']} 
                for e in enrollment
                for c in class_
                    if s['ssn'] == e['ssn']
                    if e['class'] == c['class']
                    
        ]

    def class_clean (class_=class_):
        return [{'dcode':c['dcode'], 'cno':c['cno'], 'class':c['class']}
            for c in class_
        ]

    query_k = ra.distinct([
        {'ssn' : e['ssn']}
        for e in enrollment
            if all ([x in student_enrollment(e)
                    for x in class_clean()
            ])
    ])

    #[OK] query_l

    # Helper
    def mth_class_clean ():
        return [{'dcode':c['dcode'], 'cno':c['cno']}
            for c in class_
            if c['dcode'] == "MTH"
        ]

    def cs_student_enrollment(a):
        return [{'dcode':c['dcode'], 'cno':c['cno']} 
                for e in enrollment
                for c in class_
                    if a['ssn'] == e['ssn']
                    if e['class'] == c['class']

        ]

    query_l = ra.distinct([ {"ssn": e['ssn']}
        for e in enrollment
        for s in student
        if e['ssn'] == s['ssn']
        if s['major'] == 'CS'
        if all([x in cs_student_enrollment(s)
                for x in mth_class_clean()
        ]) 
    
    ])


    # ---------------------------------------------------------------
    # Some post-processing which you do not need to worry about
    # Do not change anything after this

    ra.sortTable(query_a,["ssn"])
    ra.sortTable(query_a,["ssn"])
    ra.sortTable(query_b,["ssn"])
    ra.sortTable(query_c, ['ssn'])
    ra.sortTable(query_d, ['ssn'])
    ra.sortTable(query_e, ['ssn'])
    ra.sortTable(query_f, ['dcode', 'cno'])
    ra.sortTable(query_g, ['dcode', 'cno'])
    ra.sortTable(query_h, ['class'])
    ra.sortTable(query_i, ['ssn'])
    ra.sortTable(query_j, ['ssn'])
    ra.sortTable(query_k, ['ssn'])
    ra.sortTable(query_l, ['ssn'])

    return({
        "query_a": query_a,
        "query_b": query_b,
        "query_c": query_c,
        "query_d": query_d,
        "query_e": query_e,
        "query_f": query_f,
        "query_g": query_g,
        "query_h": query_h,
        "query_i": query_i,
        "query_j": query_j,
        "query_k": query_k,
        "query_l": query_l,

    })
