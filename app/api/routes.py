# API routes placeholder

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "AI Customer Support Agent Backend is running"}
