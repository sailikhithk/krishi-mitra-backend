from functools import wraps
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.auth import get_current_user
from app.models.user import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def requires_role(*allowed_roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = await get_current_user(Depends(oauth2_scheme))
            if current_user.role not in [UserRole(role) for role in allowed_roles]:
                raise HTTPException(status_code=403, detail="Forbidden")
            return await func(*args, **kwargs)
        return wrapper
    return decorator