import asyncio
import json

from ollama import AsyncClient
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import StreamingResponse

MODEL = "deepseek-r1:1.5b"

class UserMessageModel(BaseModel):
    content: str
app = FastAPI()

async def writing_response(message: dict[str, str]):
    client = AsyncClient()

    async for part in await client.chat(model=MODEL,
                                        messages=[message],
                                        # keep_alive=True,
                                        stream=True,
                                        think=False):
        yield part.message.content

@app.post("/")
async def index(message: UserMessageModel):
    message = {'role': 'user',
               'content': message.content}

    return StreamingResponse(
            writing_response(message),
            media_type="text/event-stream"
        )
