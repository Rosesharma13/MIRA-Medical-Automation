import re
import calendar
from datetime import date, datetime

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def validate_date_of_birth(dob_str):
    """
    Strictly validates date of birth.
    Rejects: future dates, impossible dates (e.g. Nov 31),
    non-existent dates, wrong formats.
    """
    dob_str = str(dob_str).strip()

    # Must match YYYY-MM-DD format exactly
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', dob_str):
        return False, "Invalid date format. Use YYYY-MM-DD (e.g. 1990-06-15)."

    try:
        year, month, day = map(int, dob_str.split('-'))
    except ValueError:
        return False, "Invalid date. Please enter a real calendar date."

    # Validate month range
    if month < 1 or month > 12:
        return False, f"Invalid month '{month}'. Month must be between 01 and 12."

    # Validate day range against actual days in that month/year
    max_day = calendar.monthrange(year, month)[1]
    if day < 1 or day > max_day:
        month_name = calendar.month_name[month]
        return False, (
            f"Invalid date: {month_name} {year} only has {max_day} days. "
            f"Day '{day}' does not exist."
        )

    # Try parsing as a real date
    try:
        dob = datetime(year, month, day).date()
    except ValueError:
        return False, "Invalid date. Please enter a real calendar date."

    # Must not be today or future
    if dob >= date.today():
        return False, "Date of birth cannot be today or a future date."

    # Must be within reasonable age range
    age = (date.today() - dob).days / 365.25
    if age > 120:
        return False, "Please enter a valid date of birth (max age 120 years)."

    return True, ""

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
