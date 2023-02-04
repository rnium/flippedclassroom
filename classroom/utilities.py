def prettify_marks(marks_raw):
    marks_int = int(marks_raw)
    if marks_int != marks_raw:
        return round(marks_raw, 2)
    else:
        return marks_int


def get_float_or_none(num_string):
    if num_string != None:
        try:
            num = float(num_string)
        except ValueError:
            return None
        return num
    else:
        return None
    
    
def prepare_excel_file_data(meta):
    data = []
    header = ['Name', 
              'Registration No', 
              f"Attendance ({meta.get_attendance_marks})",
              f"Class Test ({meta.get_classtest_marks})",
              f"Group Tasks ({meta.get_group_task_marks})",
              f"Individual Tasks ({meta.get_indiv_task_marks})",
              f"Tests ({meta.get_weekly_test_marks})",
              f"Total ({meta.total_marks})"]
    data.append(header)
    for a in meta.assessments:
        unit = []
        unit.append(a.student.account.user_full_name)
        unit.append(a.student.account.institutional_id)
        if a.attendance_score != None:
            unit.append(a.get_attendance_score)
        else:
            unit.append('pending')
        if a.classtest_score != None:
            unit.append(a.get_classtest_score)
        else:
            unit.append('pending')
        if a.group_task_score != None:
            unit.append(a.group_task_score)
        else:
            unit.append('pending')
        if a.indiv_task_score != None:
            unit.append(a.indiv_task_score)
        else:
            unit.append('pending')
        if a.weekly_tests_score != None:
            unit.append(a.weekly_tests_score)
        else:
            unit.append('pending')
        if a.total_score != None:
            unit.append(a.total_score)
        else:
            unit.append('pending')
        data.append(unit)
    return data