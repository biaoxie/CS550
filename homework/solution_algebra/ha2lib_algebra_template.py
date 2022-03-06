import sys
sys.path.append('..')

import lib.rel_algebra_calculus.rel_algebra_calculus as ra


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
    # Your condition functions or other helper functions (if needed)


    # ---------------------------------------------------------------
    # Your queries

    # OK query_a

    trans_cs = ra.sel(transcript, lambda x: x['dcode'] == 'CS')
    trans_cs_530 = ra.sel(trans_cs, lambda x: x['cno'] == 530)

    student_join_trans_cs_530 = ra.join(student, trans_cs_530)

    query_a = ra.proj(student_join_trans_cs_530, [
                      'ssn', 'name', 'major', 'status'])

    # OK query_b
    #student_cs_530_named_John = ra.sel(student_cs_530, lambda x: x['name'] == 'John')

    cs_530_john = ra.sel(student_join_trans_cs_530,
                         lambda x: x['name'] == 'John')
    query_b = ra.proj(cs_530_john, ['ssn', 'name', 'major', 'status'])

    # query_c

    query_c = [{"tbd": "tbd"}]

    # query_d
    query_d = [{"tbd": "tbd"}]

    # query_e
    query_e = [{"tbd": "tbd"}]

    # DONE query_f no pre-req
    course_proj = ra.proj(course, ['dcode', 'cno'])
    prereq_proj = ra.proj(prereq, ['dcode', 'cno'])

    course_no_prereq = ra.diff(course_proj, prereq_proj)

    query_f = ra.proj(course_no_prereq, ['dcode', 'cno'])

    # DONE query_g pre-req

    query_g = ra.diff(prereq_proj, query_f)

    # query_h pre-req && this semester

    query_h = [{"tbd": "tbd"}]

    # OK query_i

    transcript_c = ra.sel(transcript, lambda x: x['grade'] == 'C')
    transcript_f = ra.sel(transcript, lambda x: x['grade'] == 'F')
    transcript_cf = ra.union(transcript_c, transcript_f)

    transcript_ab = ra.diff(transcript, transcript_c)
    transcript_ab = ra.diff(transcript_ab, transcript_f)

    student_ab = ra.diff(
        ra.proj(student, ['ssn']), ra.proj(transcript_cf, ['ssn']))

    query_i = ra.join(student_ab, student)

    # OK query_j

    enroll_class = ra.join(enrollment, class_)
    enroll_class_student = ra.join(enroll_class, student)

    brodsky = ra.sel(faculty, lambda x: x['name'] == 'Brodsky')

    brodsky = ra.ren(ra.proj(brodsky, ['ssn', 'name']), {
                     'ssn': 'instr_ssn', 'name': 'instr_name'})

    enroll_class_student = ra.ren(enroll_class_student, {'instr': 'instr_ssn'})

    enroll_class_student_brodsky = ra.join(enroll_class_student, brodsky)

    query_j = ra.proj(enroll_class_student_brodsky, [
                      'ssn', 'name', 'major', 'status'])
    #query_j = enroll_class_student

    # DONE query_k

    enroll_class = ra.join(enrollment, class_)
    enroll_class = ra.join(enroll_class, course)
    enroll_class = ra.proj(enroll_class, ['ssn', 'dcode', 'cno'])

    class_course = ra.join(class_, course)
    class_course = ra.proj(class_course, ['dcode', 'cno'])

    student_completed_all = ra.div(
        enroll_class, class_course,  ['dcode', 'cno'])

    query_k = ra.proj(student_completed_all, ['ssn'])

    # query_l

    enroll_class = ra.join(enrollment, class_)
    enroll_class = ra.join(enroll_class, course)
    enroll_class = ra.join(enroll_class, student)
    cs_enroll_student = ra.sel(enroll_class, lambda x: x['major'] == 'CS')
    #cs_enroll_student = ra.proj(cs_enroll_student, ['ssn', 'dcode', 'cno'])

    class_course = ra.join(class_, course)
    math_class = ra.sel(class_course, lambda x: x['dcode'] == 'MTH')
    math_class = ra.proj(math_class, ['dcode', 'cno'])

    cs_enroll_math = ra.div(cs_enroll_student, math_class,  ['dcode', 'cno'])

    #query_l = enroll_class
    query_l =  ra.proj(cs_enroll_math, ['ssn'])

    # ---------------------------------------------------------------
    # Some post-processing which you do not need to worry about
    # Do not change anything after this

    query_a = ra.distinct(query_a)
    query_b = ra.distinct(query_b)
    query_c = ra.distinct(query_c)
    query_d = ra.distinct(query_d)
    query_e = ra.distinct(query_e)
    query_f = ra.distinct(query_f)
    query_g = ra.distinct(query_g)
    query_h = ra.distinct(query_h)
    query_i = ra.distinct(query_i)
    query_j = ra.distinct(query_j)
    query_k = ra.distinct(query_k)
    query_l = ra.distinct(query_l)


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
        "query_l": query_l
    })
