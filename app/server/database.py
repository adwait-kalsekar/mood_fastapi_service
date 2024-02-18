import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb+srv://kalsekaradwait:supersecretpassword@cluster0.fpzwdox.mongodb.net/?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.post_prompts

post_prompt_collection = database.get_collection("post_prompt_collection")

# helpers


def post_prompt_helper(post_prompt) -> dict:
    return {
        "id": str(post_prompt["_id"]),
        "prompt1": post_prompt["prompt1"],
        "prompt2": post_prompt["prompt2"],
        "image_url": post_prompt["image_url"],
        "user_email": post_prompt["email"]
    }

async def retrieve_post_prompts():
    post_prompts = []
    async for post_prompt in post_prompt_collection.find():
        post_prompt.append(post_prompt_helper(post_prompt))
    return post_prompts


async def add_post_prompt(post_prompt_data: dict) -> dict:
    post_prompt = await post_prompt_collection.insert_one(post_prompt_data)
    new_post_prompt = await post_prompt_collection.find_one({"_id": post_prompt.inserted_id})
    return post_prompt_helper(new_post_prompt)


async def retrieve_post_prompt(id: str) -> dict:
    post_prompt = await post_prompt_collection.find_one({"_id": ObjectId(id)})
    if post_prompt:
        return post_prompt_helper(post_prompt)


async def update_post_prompt(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    post_prompt = await post_prompt_collection.find_one({"_id": ObjectId(id)})
    if post_prompt:
        updated_post_prompt = await post_prompt_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_post_prompt:
            return True
        return False

async def delete_post_prompt(id: str):
    post_prompt = await post_prompt_collection.find_one({"_id": ObjectId(id)})
    if post_prompt:
        await post_prompt_collection.delete_one({"_id": ObjectId(id)})
        return True