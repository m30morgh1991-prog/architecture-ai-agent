"""Fail-closed classification of runtime failure codes.

Unknown and malformed codes are blocking. Only exact, explicitly allow-listed
non-blocking codes may be treated as non-blocking.
"""

BLOCKING = {
    "LOCKED_ELEMENT_CONFLICT",
    "POST_EDIT_REJECTED",
    "POST_EDIT_UNAUTHORIZED_DELTA",
    "NO_CAPABLE_PROVIDER",
    "PROVIDER_ADAPTER_MISSING",
}

# Keep this list intentionally small. A suffix or malformed value is not
# accepted as a non-blocking variant.
NON_BLOCKING = {
    "TARGET_NOT_FOUND",
}


def classify(failure_code):
    if not isinstance(failure_code, str):
        return "BLOCKING"
    code = failure_code.strip()
    if not code:
        return "BLOCKING"
    if code in BLOCKING or any(code.startswith(f"{known}:") for known in BLOCKING):
        return "BLOCKING"
    if code in NON_BLOCKING:
        return "NON_BLOCKING"
    return "BLOCKING"
