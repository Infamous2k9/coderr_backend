"""Validation helpers for offer query parameters."""


def validate_numeric_query_params(query_params, param_names):
    """Return an error dict if any of the given params is not a valid number, else None."""
    for param in param_names:
        value = query_params.get(param)
        if value:
            try:
                float(value)
            except ValueError:
                return {param: f"'{value}' is not a valid number."}
    return None
