import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from openai import (
    APIConnectionError,
    APITimeoutError,
    APIError,
)

from server.api.upload import router as upload_router
from server.models.chat import ChatRequest
from server.services.search_service import search_documents
from server.services.llm_service import generate_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# Create FastAPI application
app = FastAPI(
    title="AI Enterprise Productivity Assistant",
    description="Backend API for the AI Enterprise Productivity Assistant",
    version="1.0.0"
)

# -----------------------------
# CORS Configuration
# -----------------------------
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Register Routers
# -----------------------------
app.include_router(upload_router)

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to AI Enterprise Productivity Assistant 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "running"
    }

@app.post("/chat")
def chat(request: ChatRequest):

    # Validate user input
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # Retrieve relevant documents
    results = search_documents(request.question)

    if results["prompt"] is None:
        return {
            "answer": "I couldn't find any relevant information in the uploaded documents.",
            "sources": []
        }

    # Generate AI response
    try:
        answer = generate_response(results["prompt"])

    except APIConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the AI service."
        )

    except APITimeoutError:
        raise HTTPException(
            status_code=503,
            detail="The AI service took too long to respond."
        )

    except APIError:
        raise HTTPException(
            status_code=503,
            detail="The AI service is currently unavailable."
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred."
        )

    return {
        "answer": answer,
        "sources": results["metadatas"]
    }