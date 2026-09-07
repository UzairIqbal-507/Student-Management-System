def calculate_result(marks):
    """
    Safely calculates total marks, maximum marks, percentage, and overall grade.
    Prevents ZeroDivisionError during bulk imports or empty marksheets.
    """
    if not marks or not isinstance(marks, dict) or len(marks) == 0:
        return 0.0, 0.0, 0.0, "N/A"

    total_marks = 0.0
    valid_subject_count = 0

    for subject, score in marks.items():
        try:
            val = float(score) if score is not None else 0.0
            total_marks += val
            valid_subject_count += 1
        except (ValueError, TypeError):
            continue

    if valid_subject_count == 0:
        return 0.0, 0.0, 0.0, "N/A"

    maximum_marks = float(valid_subject_count * 100)
    percentage = (total_marks / maximum_marks) * 100.0

    # Grade Allocation
    if percentage >= 85:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 75:
        grade = "B+"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 65:
        grade = "C+"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    return round(total_marks, 2), round(maximum_marks, 2), round(percentage, 2), grade