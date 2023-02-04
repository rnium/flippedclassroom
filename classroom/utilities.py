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