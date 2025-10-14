"""Authentication routes"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.database import get_supabase, get_supabase_auth

router = APIRouter(prefix="/auth", tags=["authentication"])

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
async def signup(request: SignupRequest):
    """Create new user account"""
    try:
        supabase_auth = get_supabase_auth()
        response = supabase_auth.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "full_name": request.full_name
                }
            }
        })

        if response.user:
            # Create user profile (using admin client to bypass RLS)
            supabase_admin = get_supabase()
            supabase_admin.table("user_profiles").insert({
                "id": response.user.id,
                "email": request.email,
                "full_name": request.full_name
            }).execute()

        return {
            "user": response.user,
            "session": response.session
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(request: LoginRequest):
    """Login user"""
    try:
        supabase_auth = get_supabase_auth()
        response = supabase_auth.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })

        return {
            "user": response.user,
            "session": response.session
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/logout")
async def logout():
    """Logout user"""
    try:
        supabase_auth = get_supabase_auth()
        supabase_auth.auth.sign_out()
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
