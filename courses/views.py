from django.http import JsonResponse
from django.db.models import Count, Avg, Max, Min
from .models import Course, Enrollment, Lesson

# ==========================================
# 1. Course + Teacher (select_related)
# ==========================================
def course_list_baseline(request):
    courses = Course.objects.all()
    data = []
    for c in courses:
        data.append({
            'course': c.title,
            'teacher': c.instructor.username # Memicu N+1
        })
    return JsonResponse({'data': data})

def course_list_optimized(request):
    courses = Course.objects.select_related('instructor').all() # Optimasi
    data = []
    for c in courses:
        data.append({
            'course': c.title,
            'teacher': c.instructor.username
        })
    return JsonResponse({'data': data})

# ==========================================
# 2. Course + Members (prefetch_related)
# ==========================================
def course_members_baseline(request):
    courses = Course.objects.all()
    payload = []
    for c in courses:
        payload.append({
            'course': c.title,
            'member_count': c.enrollment_set.count() # Memicu N+1 parah
        })
    return JsonResponse({'data': payload})

def course_members_optimized(request):
    courses = Course.objects.prefetch_related('enrollment_set').all() # Optimasi
    payload = []
    for c in courses:
        payload.append({
            'course': c.title,
            'member_count': c.enrollment_set.count()
        })
    return JsonResponse({'data': payload})

# ==========================================
# 3. Dashboard Statistik (aggregate & annotate)
# ==========================================
def course_dashboard_baseline(request):
    courses = Course.objects.all()
    total_courses = 0
    for c in courses:
        total_courses += 1 # Menghitung manual di Python (Sangat lambat)
    
    return JsonResponse({
        'total_courses': total_courses,
    })

def course_dashboard_optimized(request):
    stats = Course.objects.aggregate(total=Count('id')) # Dihitung langsung oleh Database
    return JsonResponse(stats)