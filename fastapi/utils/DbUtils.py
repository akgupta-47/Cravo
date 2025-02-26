from typing import Any, Dict


def clean_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively removes None values and empty lists from a dictionary."""
    cleaned_data = {}

    for key, value in data.items():
        if isinstance(value, dict):
            nested = clean_data(value)  # Recursively clean nested dicts
            if nested:  # Only add if not empty
                cleaned_data[key] = nested
        elif isinstance(value, list):
            filtered_list = [
                clean_data(item) if isinstance(item, dict) else item for item in value
            ]
            filtered_list = [
                item for item in filtered_list if item not in [None, {}, []]
            ]  # Remove empty items
            if filtered_list:  # Only add if not empty
                cleaned_data[key] = filtered_list
        elif value not in [None, {}]:  # Exclude None and empty dicts
            cleaned_data[key] = value

    return cleaned_data
