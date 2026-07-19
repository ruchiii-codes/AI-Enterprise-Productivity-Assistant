from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.api.upload import router as upload_router

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
