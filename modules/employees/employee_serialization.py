def employee_serialize(employee):
    return {
        "id": str(employee["_id"]),
        "name": employee["name"],
        "email": employee["email"],
        "role": employee["role"],
        "created_at": str(employee["created_at"]),
        "designation": (
            {
                "id": str(employee["designation"]["_id"]),
                "name": str(employee["designation"]["name"]),
            }
            if "designation" in employee and employee["designation"]
            else None
        ),
        "department": (
            {
                "id": str(employee["department"]["_id"]),
                "name": str(employee["department"]["name"]),
            }
            if "department" in employee and employee["department"]
            else None
        ),
    }
