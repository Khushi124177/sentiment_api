from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
import json

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
                    "content": "Return ONLY valid JSON like {\"sentiment\":\"positive\",\"rating\":5}. No extra text."
                },
                {
                    "role": "user",
                    "content": request.comment
                }
            ],
            temperature=0
        )

        content = completion.choices[0].message.content.strip()

        # Safe JSON extraction
        start = content.find("{")
        end = content.rfind("}") + 1
        json_string = content[start:end]

        result = json.loads(json_string)

        # Extra safety (avoid invalid values)
        if result["sentiment"] not in ["positive", "negative", "neutral"]:
            result["sentiment"] = "neutral"

        result["rating"] = max(1, min(5, int(result["rating"])))

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail="Processing error")
