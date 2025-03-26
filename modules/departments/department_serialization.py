def department_serialize(department):
    return {"id": str(department["_id"]), "name": str(department["name"])}
