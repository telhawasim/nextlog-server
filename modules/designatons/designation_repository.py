from bson import ObjectId
from app.exception import CustomException
from app.mongodb import db
from .designation_serialization import designation_serialize
from .designation_response_models import GetAllDesignationsModel, GetDesignationModel
from .designation_request_models import AddDesignationModel
from .designation import Designation
from modules.shared.models import BaseServerModel


async def get_all():
    # Extract all the designations
    designations_cursor = db.designations.find()
    # Make them as a list
    designations = await designations_cursor.to_list(length=None)
    # Serialize the response according to requirement
    serialzied_designations = [
        designation_serialize(designation) for designation in designations
    ]
    # Response
    return GetAllDesignationsModel(designations=serialzied_designations)


async def get(id):
    # Validate the ID
    if not ObjectId.is_valid(id):
        raise CustomException(status_code=400, message="Invalid ID")
    # Extract designation if it already exists in database
    designation = await db.designations.find_one({"_id": ObjectId(id)})
    # Throw exception if there is no designation with respect to ID
    if not designation:
        raise CustomException(status_code=404, message="Designation doesn't exist")
    return GetDesignationModel(id=str(designation["_id"]), name=designation["name"])


async def add(request: AddDesignationModel):
    # Validate the request
    request.add_desigantion_validation()
    # Extract designation if it is already available in database
    designation = await db.designations.find_one({"name": request.name})
    # Throw exception if designation with same name already exists
    if designation:
        raise CustomException(status_code=404, message="Designation already exists")
    # Add new object for the designation
    new_designation = Designation(name=request.name)
    # Insert the object in the database
    await db.designations.insert_one(new_designation.model_dump())
    # Response
    return BaseServerModel(
        status=200, message="Designation has been added successfully"
    )


async def delete(id):
    # Validate the ID
    if not ObjectId.is_valid(id):
        raise CustomException(status_code=400, message="Invalid ID")
    # Extract designation if it already available in database
    designation = await db.designations.find_one_and_delete({"_id": ObjectId(id)})
    # Throw exception if there is no designation with respect to ID
    if not designation:
        raise CustomException(status_code=404, message="Designation doesn't exist")
    # Response
    return BaseServerModel(
        status=200, message="Designation has been deleted successfully"
    )
