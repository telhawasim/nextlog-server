def designation_serialize(designation):
    return {"id": str(designation["_id"]), "name": str(designation["name"])}
