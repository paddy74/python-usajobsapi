from typing import Any, Dict, Optional

from pydantic import BaseModel


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
        # Skip empty lists
        return ";".join(map(str, value)) if value else None
    # Everything else as a string
    return str(value)


def _dump_by_alias(model: BaseModel) -> Dict[str, str]:
    """Dump a Pydantic model to a query-param dict using the model's field aliases and USAJOBS formatting rules (lists + bools).

    :param model: _description_
    :type model: BaseModel
    :return: _description_
    :rtype: Dict[str, str]
    """
    # Use the API's wire names and drop `None`s
    raw = model.model_dump(by_alias=True, exclude_none=True, mode="json")

    # Normalize values
    out: Dict[str, str] = {}
    for k, v in raw.items():
        norm_val = _normalize_param(v)
        if norm_val:
            out[k] = norm_val
    return out
