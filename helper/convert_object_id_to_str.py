from bson import ObjectId


def convert_object_id_to_str(obj):
    if isinstance(obj, list):
        return [convert_object_id_to_str(item) for item in obj]
    elif isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            if key == "_id":
                new_obj["id"] = str(value)
            else:
                new_obj[key] = convert_object_id_to_str(value)
        return new_obj
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj
