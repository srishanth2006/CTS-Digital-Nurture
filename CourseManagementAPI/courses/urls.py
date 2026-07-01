"""
URL routing for the courses app.

- PART 3/4: DefaultRouter wires up ModelViewSets for the production API
  (/api/departments/, /api/students/, /api/courses/, /api/enrollments/),
  including the custom /api/courses/<id>/students/ action.
- PART 1: Function-based view demo routes live under /api/fbv/.
- PART 2: Class-based view demo routes live under /api/cbv/.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from courses import views

app_name = "courses"

# ------------------------------------------------------------------------------
# PART 3 & 4: ViewSets + DefaultRouter (production endpoints)
# ------------------------------------------------------------------------------
router = DefaultRouter()
router.register("departments", views.DepartmentViewSet, basename="department")
router.register("students", views.StudentViewSet, basename="student")
router.register("courses", views.CourseViewSet, basename="course")
router.register("enrollments", views.EnrollmentViewSet, basename="enrollment")

urlpatterns = [
    # ViewSet-powered production API (Parts 3 & 4)
    path("", include(router.urls)),

    # PART 1: Function-Based Views (Department demonstration)
    path("fbv/departments/", views.department_list, name="fbv-department-list"),
    path("fbv/departments/<int:pk>/", views.department_detail, name="fbv-department-detail"),

    # PART 2: Class-Based Views (Student demonstration)
    path("cbv/students/", views.StudentAPIView.as_view(), name="cbv-student-apiview"),
    path(
        "cbv/students/generic/",
        views.StudentListCreateAPIView.as_view(),
        name="cbv-student-list-create",
    ),
    path(
        "cbv/students/generic/<int:pk>/",
        views.StudentRetrieveUpdateDestroyAPIView.as_view(),
        name="cbv-student-detail",
    ),
]
