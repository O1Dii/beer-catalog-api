def wrap_data(data: dict, wrapping_field_name: str, wrapped_fields: list) -> dict:
    data[wrapping_field_name] = {}

    for field in wrapped_fields:
        data[wrapping_field_name][field] = data[field]

    def filter_function(item):
        if item[0] in wrapped_fields:
            return False

        return True

    return dict(filter(filter_function, data.items()))


def unwrap_data(data: dict, wrapping_field_name: str) -> dict:
    for item in data[wrapping_field_name].items():
        data[item[0]] = item[1]

    del data[wrapping_field_name]

    return data
