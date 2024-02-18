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

@router.post("/", response_description="PostPrompt data added into the database")
async def add_post_prompt_data(post_prompt: PostPromptSchema = Body(...)):
    post_prompt = jsonable_encoder(post_prompt)
    new_post_prompt = await add_post_prompt(post_prompt)
    return ResponseModel(new_post_prompt, "PostPrompt added successfully.")

@router.get("/", response_description="PostPrompts retrieved")
async def get_post_prompt():
    post_prompts = await retrieve_post_prompts()
    if post_prompts:
        return ResponseModel(post_prompts, "PostPrompts data retrieved successfully")
    return ResponseModel(post_prompts, "Empty list returned")


@router.get("/{id}", response_description="PostPrompt data retrieved")
async def get_post_prompt_data(id):
    post_prompt = await retrieve_post_prompt(id)
    if post_prompt:
        return ResponseModel(post_prompt, "PostPrompt data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "PostPrompt doesn't exist.")

@router.put("/{id}")
async def update_post_prompt_data(id: str, req: UpdatePostPromptModel = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_post_prompt = await update_post_prompt(id, req)
    if updated_post_prompt:
        return ResponseModel(
            "PostPrompt with ID: {} name update is successful".format(id),
            "PostPrompt name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the post_prompt data.",
    )

@router.delete("/{id}", response_description="PostPrompt data deleted from the database")
async def delete_post_prompt_data(id: str):
    deleted_post_prompt = await delete_post_prompt(id)
    if deleted_post_prompt:
        return ResponseModel(
            "PostPrompt with ID: {} removed".format(id), "PostPrompt deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "PostPrompt with id {0} doesn't exist".format(id)
    )