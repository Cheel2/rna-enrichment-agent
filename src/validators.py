"""Validation des identifiants RNA."""
import re

RNA_PATTERN = re.compile(r'^W\d{9}$')

def is_valid_rna(rna):
    if not rna:
        return False
    return bool(RNA_PATTERN.match(str(rna).strip()))
