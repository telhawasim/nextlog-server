def admin_serialize(admin):
    return {
        "id": str(admin["_id"]),
        "email": str(admin["email"]),
        "role": str(admin["role"]),
    }
