def employee_serialize(employee):
    return {
        "id": str(employee["_id"]),
        "name": str(employee["name"]),
        "email": str(employee["email"]),
        "role": str(employee["role"]),
        "created_at": str(employee["created_at"]),
    }
