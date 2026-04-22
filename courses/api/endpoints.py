from ninja import NinjaAPI, Router
from ninja.pagination import paginate
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .schemas import *
from .security import GlobalAuth, create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM, AuthError
from courses.models import User, Course, Enrollment, Progress, Lesson
from jose import jwt

api = NinjaAPI(title="Simple LMS API", version="1.0.0", description="REST API for Simple LMS")

# --- Custom Exception Handler ---
@api.exception_handler(AuthError)
def auth_error_handler(request, exc):
    return api.create_response(request, {"detail": str(exc)}, status=403)

# ==========================================
# 1. AUTHENTICATION ROUTER
# ==========================================
auth_router = Router()

@auth_router.post("/register", response=UserOut, auth=None)
def register(request, data: RegisterIn):
    user = User.objects.create_user(
        username=data.username, 
        password=data.password, 
        email=data.email, 
        role=data.role
    )
    return user

@auth_router.post("/login", response=TokenOut, auth=None)
def login(request, data: LoginIn):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return api.create_response(request, {"detail": "Invalid credentials"}, status=401)
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id)
    }

@auth_router.post("/refresh", response=TokenOut, auth=None)
def refresh_token(request, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise AuthError("Invalid token type")
        user_id = payload.get("user_id")
        return {"access_token": create_access_token(user_id), "refresh_token": refresh_token}
    except jwt.JWTError:
        return api.create_response(request, {"detail": "Invalid or expired refresh token"}, status=401)

@auth_router.get("/me", response=UserOut, auth=GlobalAuth())
def get_me(request):
    return request.auth

@auth_router.put("/me", response=UserOut, auth=GlobalAuth())
def update_me(request, data: UserUpdateIn):
    user = request.auth
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(user, attr, value)
    user.save()
    return user

# ==========================================
# 2. COURSES ROUTER
# ==========================================
course_router = Router()

@course_router.get("/", response=List[CourseOut], auth=None)
@paginate
def list_courses(request, category_id: int = None):
    qs = Course.objects.all()
    if category_id:
        qs = qs.filter(category_id=category_id)
    return qs

@course_router.get("/{id}", response=CourseOut, auth=None)
def get_course(request, id: int):
    return get_object_or_404(Course, id=id)

@course_router.post("/", response=CourseOut, auth=GlobalAuth())
def create_course(request, data: CourseCreateIn):
    if request.auth.role != 'instructor':
        raise AuthError("Only instructors can create courses.")
    course = Course.objects.create(instructor=request.auth, **data.dict())
    return course

@course_router.patch("/{id}", response=CourseOut, auth=GlobalAuth())
def update_course(request, id: int, data: CourseUpdateIn):
    course = get_object_or_404(Course, id=id)
    if course.instructor != request.auth:
        raise AuthError("Only the owner can update this course.")
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(course, attr, value)
    course.save()
    return course

@course_router.delete("/{id}", auth=GlobalAuth())
def delete_course(request, id: int):
    if request.auth.role != 'admin':
        raise AuthError("Only admins can delete courses.")
    course = get_object_or_404(Course, id=id)
    course.delete()
    return {"success": True, "message": "Course deleted"}

# ==========================================
# 3. ENROLLMENTS ROUTER
# ==========================================
enroll_router = Router(auth=GlobalAuth())

@enroll_router.post("/", response=dict)
def enroll_to_course(request, data: EnrollmentIn):
    if request.auth.role != 'student':
        raise AuthError("Only students can enroll in courses.")
    course = get_object_or_404(Course, id=data.course_id)
    Enrollment.objects.get_or_create(student=request.auth, course=course)
    return {"success": True, "message": "Enrolled successfully"}

@enroll_router.get("/my-courses", response=List[EnrollmentOut])
def my_courses(request):
    return Enrollment.objects.filter(student=request.auth)

@enroll_router.post("/{enrollment_id}/progress", response=dict)
def mark_progress(request, enrollment_id: int, data: ProgressIn):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.auth)
    lesson = get_object_or_404(Lesson, id=data.lesson_id, course=enrollment.course)
    progress, _ = Progress.objects.get_or_create(student=request.auth, lesson=lesson)
    progress.is_completed = True
    progress.save()
    return {"success": True, "message": "Lesson marked as complete"}

# --- Register Routers to API ---
api.add_router("/auth", auth_router, tags=["Authentication"])
api.add_router("/courses", course_router, tags=["Courses"])
api.add_router("/enrollments", enroll_router, tags=["Enrollments"])