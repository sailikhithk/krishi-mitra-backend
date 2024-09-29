from functools import wraps
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.auth import get_current_user
from app.models.user import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def requires_role(*allowed_roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = await get_current_user(token=Depends(oauth2_scheme))
            print(f"Current user role: {current_user.role}")
            print(f"Allowed roles: {allowed_roles}")
            if current_user.role not in allowed_roles:
                raise HTTPException(status_code=403, detail="Forbidden")
            return await func(current_user=current_user, *args, **kwargs)
        return wrapper
    return decorator

def admin_required():
    return requires_role("admin")