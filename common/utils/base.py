import copy
import json


def remove_none(dto):
    if isinstance(dto, str):
        dto = json.loads(dto)

    dto_copy = copy.deepcopy(dto)

    keys_to_remove = []
    for key, value in dto_copy.items():
        if value is None:
            keys_to_remove.append(key)
        elif isinstance(value, dict):
            dto_copy[key] = remove_none(value)
            if not dto_copy[key]:
                keys_to_remove.append(key)

    for key in keys_to_remove:
        del dto_copy[key]

    return dto_copy
