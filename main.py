from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommentRequest(BaseModel):
    comment: str

class CommentResponse(BaseModel):
    sentiment: str
    rating: int

@app.post("/comment", response_model=CommentResponse)
async def analyze_comment(request: CommentRequest):

    text = request.comment.lower()

    positive_words = ["good", "great", "amazing", "excellent", "love", "awesome"]
    negative_words = ["bad", "worst", "terrible", "hate", "awful", "poor"]

    score = 0

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        sentiment = "positive"
        rating = min(5, 3 + score)
    elif score < 0:
        sentiment = "negative"
        rating = max(1, 3 + score)
    else:
        sentiment = "neutral"
        rating = 3

    return {"sentiment": sentiment, "rating": rating}
