from datetime import datetime, timedelta
from jose import jwt, JWTError
from django.conf import settings
from ninja.security import HttpBearer
from django.shortcuts import get_object_or_404
from courses.models import User

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_EXP = 60      # 60 menit
REFRESH_EXP = 1440   # 1 hari

def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXP)
    return jwt.encode({"user_id": user_id, "exp": expire, "type": "access"}, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_EXP)
    return jwt.encode({"user_id": user_id, "exp": expire, "type": "refresh"}, SECRET_KEY, algorithm=ALGORITHM)

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != "access":
                return None
            user_id = payload.get("user_id")
            user = get_object_or_404(User, id=user_id)
            return user
        except (JWTError, Exception):
            return None

# Custom Error untuk Authorization
class AuthError(Exception):
    pass