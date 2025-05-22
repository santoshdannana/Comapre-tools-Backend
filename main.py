from fastapi import FastAPI
from schemas.request_response import AskRequest, AskResponse
from services.gemini_client import get_solutions
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI Solution Finder API is running"}

@app.post("/ask", response_model=AskResponse)
async def ask_question(payload: AskRequest):
    return await get_solutions(payload.question)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://compare-tools.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

