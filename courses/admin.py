from django.contrib import admin
from .models import User, Category, Course, Lesson, Enrollment, Progress

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor')
    search_fields = ('title',)
    list_filter = ('category', 'instructor')
    inlines = [LessonInline]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)

admin.site.register(Category)
admin.site.register(Enrollment)
admin.site.register(Progress)