import logging
import time
from server.services.prompt_builder import build_messages

from server.services.planner_service import (
    plan_route,
    Route,
)
from server.services.tool_service import count_uploaded_pdfs

from fastapi import FastAPI, HTTPException, Request
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

from server.services.orchestrator_service import execute

from server.auth.database import Base, engine
from server.auth import models

from server.api.auth import router as auth_router

from fastapi import Depends

from server.auth.dependencies import get_current_user
from server.auth.models import User

from server.api.conversation import (
    router as conversation_router,
)

from server.api.message import (
    router as message_router,
)

from sqlalchemy.orm import Session

from server.auth.database import get_db

from server.services.message_service import (
    add_message,
    get_recent_messages,
)

from server.services.conversation_service import (
    get_conversation,
)

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from server.utils.rate_limiter import limiter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)  
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="AI Enterprise Productivity Assistant",
    description="Backend API for the AI Enterprise Productivity Assistant",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)
app.add_middleware(SlowAPIMiddleware)

@app.middleware("http")
async def request_monitoring(request: Request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time

        logger.info(
            "HTTP %s %s - %s - %.3fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = time.perf_counter() - start_time

        logger.exception(
            "HTTP %s %s failed after %.3fs",
            request.method,
            request.url.path,
            duration,
        )

        raise

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
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
    ],
)

# -----------------------------
# Register Routers
# -----------------------------
app.include_router(upload_router)
app.include_router(auth_router)
app.include_router(conversation_router)
app.include_router(message_router)

@app.on_event("startup")
def startup_event():

    Base.metadata.create_all(bind=engine)

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
@limiter.limit("30/minute")
def chat(
    request: Request,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    logger.info("Authenticated request from user: %s", current_user.email)

    conversation = get_conversation(
        db=db,
        conversation_id=chat_request.conversation_id,
        user_id=current_user.id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )
    
    # Validate user input
    if not chat_request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    route = plan_route(chat_request.question)

    logger.info("Planner Route selected: %s", route.value)

    # -----------------------------
    # Orchestrator
    # -----------------------------
    if route != Route.DIRECT_LLM:

        result = execute(
            route=route,
            question=chat_request.question,
        )

        # Retrieval continues into chat flow
        if route == Route.RETRIEVAL:

            if result["prompt"] is None:
                return {
                    "answer": "I couldn't find any relevant information in the uploaded documents.",
                    "sources": [],
                }

            prompt = result["prompt"]
            results = {
                "metadatas": result["metadatas"],
            }
    
        # Tool & Summarization return immediately
        else:
            return result

    # -----------------------------
    # Direct LLM
    # -----------------------------
    else:

        prompt = chat_request.question

        results = {
            "metadatas": [],
        }

    # Load previous conversation history
    history = get_recent_messages(
        db=db,
        conversation_id=chat_request.conversation_id,
    )

    # Build OpenAI messages
    messages = build_messages(
        history=history,
        current_prompt=prompt,
    )

    add_message(
        db=db,
        conversation_id=chat_request.conversation_id,
        role="user",
        content=chat_request.question,
    )

    # Generate AI response
    try:
        answer = generate_response(messages)

        add_message(
            db=db,
            conversation_id=request.conversation_id,
            role="assistant",
            content=answer,
        )
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
