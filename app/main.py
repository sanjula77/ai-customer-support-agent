# Entry point for the customer support AI application

from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="AI Customer Support Agent",
    version="1.0.0"
)

# Include API routes
app.include_router(api_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

