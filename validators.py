"""validators.py — Input validators for ProbeAI"""
import re


def validate_email(v):
    return bool(re.match(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$", v)), "Please enter a valid email address."


def validate_phone(v):
    digits = re.sub(r"[\s\-\(\)\+]", "", v)
    return (7 <= len(digits) <= 15 and digits.lstrip("0").isdigit()), \
           "Please enter a valid phone number (7-15 digits)."


def validate_experience(v):
    try:
        n = float(v.split()[0])
        return 0 <= n <= 50, "Please enter years of experience (e.g. 3 or 3.5)."
    except Exception:
        return False, "Please enter a number (e.g. 2 or 5)."


VALIDATORS = {
    "email":      validate_email,
    "phone":      validate_phone,
    "experience": validate_experience,
}