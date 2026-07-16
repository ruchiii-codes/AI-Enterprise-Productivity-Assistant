from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(
    title="AI Enterprise Productivity Assistant",
    description="Backend API for the AI Enterprise Productivity Assistant",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to AI Enterprise Productivity Assistant API 🚀"
    }

# Health check endpoint
@app.get("/health")
def health():
    return {
        "status": "running"
    }