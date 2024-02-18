from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_post_prompt,
    delete_post_prompt,
    retrieve_post_prompt,
    retrieve_post_prompts,
    update_post_prompt,
)
from server.models.post_prompt import (
    ErrorResponseModel,
    ResponseModel,
    PostPromptSchema,
    UpdatePostPromptModel,
)

router = APIRouter()

@router.post("/", response_description="Student data added into the database")
async def add_student_data(student: PostPromptSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_post_prompt(student)
    return ResponseModel(new_student, "Student added successfully.")

@router.get("/", response_description="Students retrieved")
async def get_students():
    students = await retrieve_post_prompts()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")


@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id):
    student = await retrieve_post_prompt(id)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")

@router.put("/{id}")
async def update_student_data(id: str, req: UpdatePostPromptModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await update_post_prompt(id, req)
    if updated_student:
        return ResponseModel(
            "Student with ID: {} name update is successful".format(id),
            "Student name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )

@router.delete("/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id: str):
    deleted_student = await delete_post_prompt(id)
    if deleted_student:
        return ResponseModel(
            "Student with ID: {} removed".format(id), "Student deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Student with id {0} doesn't exist".format(id)
    )