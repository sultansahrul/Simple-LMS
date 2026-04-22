"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from courses.api.endpoints import api
from courses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('silk/', include('silk.urls', namespace='silk')),

    path('lab/course-list/baseline/', views.course_list_baseline),
    path('lab/course-list/optimized/', views.course_list_optimized),
    
    path('lab/course-members/baseline/', views.course_members_baseline),
    path('lab/course-members/optimized/', views.course_members_optimized),
    
    path('lab/course-dashboard/baseline/', views.course_dashboard_baseline),
    path('lab/course-dashboard/optimized/', views.course_dashboard_optimized),
]