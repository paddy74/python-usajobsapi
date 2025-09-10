from typing import Any, Optional


def _normalize_param(value: Any) -> Optional[str]:
    """Normalize query parameters to the format expected by USAJOBS.

    :param value: Query parameter to normalize
    :type value: Any
    :return: Query parameter normalized for the USAJOBS REST API.
    :rtype: Optional[str]
    """
    if value is None:
        # None -> omit
        return None
    if isinstance(value, bool):
        # bools -> 'True'/'False'
        return "True" if value else "False"
    if isinstance(value, list):
        # lists -> ';'
        return ";".join(map(str, value)) if value else None
    return str(value)
