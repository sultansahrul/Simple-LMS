from ninja import Schema, ModelSchema
from pydantic import EmailStr
from typing import List, Optional
from courses.models import Course, Enrollment

# --- AUTH SCHEMAS ---
class RegisterIn(Schema):
    username: str
    password: str
    email: EmailStr
    role: str = 'student'

class LoginIn(Schema):
    username: str
    password: str

class TokenOut(Schema):
    access_token: str
    refresh_token: str

class UserOut(Schema):
    id: int
    username: str
    email: str
    role: str

class UserUpdateIn(Schema):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

# --- COURSE SCHEMAS ---
class CourseOut(ModelSchema):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description']

class CourseCreateIn(Schema):
    title: str
    description: str
    category_id: int

class CourseUpdateIn(Schema):
    title: Optional[str] = None
    description: Optional[str] = None

# --- ENROLLMENT SCHEMAS ---
class EnrollmentIn(Schema):
    course_id: int

class EnrollmentOut(ModelSchema):
    course: CourseOut
    class Meta:
        model = Enrollment
        fields = ['id', 'course']

class ProgressIn(Schema):
    lesson_id: int