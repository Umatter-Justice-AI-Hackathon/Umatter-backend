from fastapi import APIRouter
# from app.api.v1 import auth, users

api_router = APIRouter()

# Include routers here
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])


@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "UMatter Backend is running"}
