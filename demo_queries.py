import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Course

def run_demo():
    print("--- DEMO OPTIMASI QUERY (N+1 PROBLEM) ---")
    
    # 1. Tanpa Optimasi
    print("\n[Executing Non-Optimized Query...]")
    courses = Course.objects.all()
    for c in courses:
        print(f"Course: {c.title}, Category: {c.category.name}") # Ini trigger query ke DB setiap iterasi
    print(f"Total Queries (Non-Optimized): {len(connection.queries)}")

    connection.queries_log.clear()

    # 2. Dengan Optimasi
    print("\n[Executing Optimized Query (select_related)...]")
    courses_opt = Course.objects.for_listing()
    for c in courses_opt:
        print(f"Course: {c.title}, Category: {c.category.name}")
    print(f"Total Queries (Optimized): {len(connection.queries)}")

if __name__ == "__main__":
    run_demo()