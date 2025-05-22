from pydantic import BaseModel
from typing import List

class Solution(BaseModel):
    name: str
    description: str
    pros: List[str]
    cons: List[str]
    pricing: str
    link: str

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    question: str
    solutions: List[Solution]
