from fastapi import FastAPI

from server.routes.post_prompt import router as PostPromptRouter

app = FastAPI()

app.include_router(PostPromptRouter, tags=["PostPrompt"], prefix="/api/v1/post_prompt")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "api is running"}

