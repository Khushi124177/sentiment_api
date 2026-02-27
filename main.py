from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import json

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CommentRequest(BaseModel):
    comment: str

class CommentResponse(BaseModel):
    sentiment: str
    rating: int

@app.post("/comment", response_model=CommentResponse)
async def analyze_comment(request: CommentRequest):
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze sentiment and respond ONLY in JSON format like: {\"sentiment\": \"positive\", \"rating\": 5}"
                },
                {
                    "role": "user",
                    "content": request.comment
                }
            ],
            temperature=0
        )

        content = completion.choices[0].message.content
        result = json.loads(content)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
