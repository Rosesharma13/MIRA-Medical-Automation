import re
from datetime import date, datetime

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def validate_date_of_birth(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        if dob >= date.today():
            return False, "Date of birth cannot be today or a future date."
        age = (date.today() - dob).days / 365.25
        if age > 120:
            return False, "Please enter a valid date of birth."
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD."

def validate_numeric(value, field_name, min_val=0, max_val=9999):
    try:
        val = float(value)
        if val < min_val or val > max_val:
            return False, f"{field_name} must be between {min_val} and {max_val}."
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} must be a numeric value."

def validate_patient_form(full_name, dob, email, glucose, haemoglobin, cholesterol):
    errors = []

    if not full_name or len(full_name.strip()) < 2:
        errors.append("Full name must be at least 2 characters.")

    dob_valid, dob_msg = validate_date_of_birth(str(dob))
    if not dob_valid:
        errors.append(dob_msg)

    if not validate_email(email):
        errors.append("Invalid email address format.")

    g_valid, g_msg = validate_numeric(glucose, "Glucose", 0, 600)
    if not g_valid:
        errors.append(g_msg)

    h_valid, h_msg = validate_numeric(haemoglobin, "Haemoglobin", 0, 25)
    if not h_valid:
        errors.append(h_msg)

    c_valid, c_msg = validate_numeric(cholesterol, "Cholesterol", 0, 700)
    if not c_valid:
        errors.append(c_msg)

    return errors
