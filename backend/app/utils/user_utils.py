"""User utility functions"""

from typing import Dict
from ..database import get_supabase


async def ensure_user_profile(user_id: str, email: str = None, full_name: str = None) -> Dict:
    """
    Ensure a user profile exists, creating a default one if missing

    Args:
        user_id: User's UUID
        email: Optional email to use for new profile
        full_name: Optional name to use for new profile

    Returns:
        User profile dict
    """
    supabase = get_supabase()

    # Check if profile exists
    result = supabase.table("user_profiles")\
        .select("*")\
        .eq("id", user_id)\
        .execute()

    if result.data and len(result.data) > 0:
        return result.data[0]

    # Profile doesn't exist - create default
    print(f"Creating default profile for user {user_id}")

    # Try to get email from auth.users if not provided
    if not email:
        try:
            auth_result = supabase.table("users")\
                .select("email")\
                .eq("id", user_id)\
                .single()\
                .execute()
            email = auth_result.data.get("email", "user@example.com")
        except:
            email = "user@example.com"

    default_profile = {
        "id": user_id,
        "full_name": full_name or "User",
        "email": email,
        "preferred_language": "en",
        "onboarding_completed": False
    }

    try:
        insert_result = supabase.table("user_profiles").insert(default_profile).execute()
        print(f"Created profile for user {user_id}")
        return insert_result.data[0]
    except Exception as e:
        print(f"Error creating profile: {e}")
        # Return default dict to prevent crashes
        return default_profile
