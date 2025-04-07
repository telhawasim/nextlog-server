from bson import ObjectId


def convert_object_id_to_str(doc):
    if isinstance(doc, dict):
        return {key: convert_object_id_to_str(value) for key, value in doc.items()}
    elif isinstance(doc, list):
        return [convert_object_id_to_str(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc
