"""
Views for the Course Management API.

This module demonstrates three different DRF approaches as required by the
hands-on exercise:

    PART 1 - Function-Based Views      -> department_list, department_detail
    PART 2 - Class-Based Views (CBV)   -> StudentListCreateAPIView,
                                           StudentRetrieveUpdateDestroyAPIView
    PART 3 - ViewSets (production API) -> DepartmentViewSet, StudentViewSet,
                                           CourseViewSet, EnrollmentViewSet

The ViewSets (registered with a DefaultRouter in courses/urls.py) power the
primary /api/departments/, /api/students/, /api/courses/, /api/enrollments/
endpoints listed in the project's API documentation. The FBV and CBV
implementations are kept as standalone demonstration endpoints under
/api/fbv/ and /api/cbv/ respectively, mirroring the progressive structure of
the exercise book (Task 1 builds FBV/CBV, Task 2 refactors to ViewSets).
"""

from django.shortcuts import get_object_or_404
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Department, Student, Course, Enrollment
from courses.serializers import (
    DepartmentSerializer,
    StudentSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    CourseStudentsSerializer,
)


# ==============================================================================
# PART 1: FUNCTION-BASED VIEWS (Department demonstration endpoints)
# ==============================================================================

@api_view(["GET", "POST"])
def department_list(request):
    """
    GET  /api/fbv/departments/  -> list all departments
    POST /api/fbv/departments/  -> create a new department
    """
    if request.method == "GET":
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def department_detail(request, pk):
    """
    GET    /api/fbv/departments/<pk>/  -> retrieve a single department
    PUT    /api/fbv/departments/<pk>/  -> update a department
    DELETE /api/fbv/departments/<pk>/  -> delete a department
    """
    department = get_object_or_404(Department, pk=pk)

    if request.method == "GET":
        serializer = DepartmentSerializer(department)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    department.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ==============================================================================
# PART 2: CLASS-BASED VIEWS (Student demonstration endpoints)
# ==============================================================================

class StudentAPIView(APIView):
    """
    Plain APIView demonstrating explicit HTTP method handling for Student.

    GET  /api/cbv/students/  -> list all students
    POST /api/cbv/students/  -> create a new student
    """

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentListCreateAPIView(generics.ListCreateAPIView):
    """
    Generic ListCreateAPIView for Student.

    GET  /api/cbv/students/generic/  -> list all students
    POST /api/cbv/students/generic/  -> create a new student
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    search_fields = ["name", "email"]
    ordering_fields = ["name", "email"]


class StudentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic RetrieveUpdateDestroyAPIView for Student.

    GET    /api/cbv/students/generic/<pk>/  -> retrieve a student
    PUT    /api/cbv/students/generic/<pk>/  -> update a student
    PATCH  /api/cbv/students/generic/<pk>/  -> partially update a student
    DELETE /api/cbv/students/generic/<pk>/  -> delete a student
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# ==============================================================================
# PART 3: VIEWSETS (production API, wired up via DefaultRouter)
# ==============================================================================

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Full CRUD ViewSet for Department.

    Provides: list, create, retrieve, update, partial_update, destroy
    Registered at /api/departments/ via the DefaultRouter.
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ["name"]
    ordering_fields = ["name", "id"]

    @action(detail=True, methods=["get"], url_path="courses")
    def department_courses(self, request, pk=None):
        """GET /api/departments/<id>/courses/ -> all courses in this department."""
        department = self.get_object()
        courses = department.courses.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="students")
    def department_students(self, request, pk=None):
        """GET /api/departments/<id>/students/ -> all students in this department."""
        department = self.get_object()
        students = department.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentViewSet(viewsets.ModelViewSet):
    """
    Full CRUD ViewSet for Student.

    Provides: list, create, retrieve, update, partial_update, destroy
    Registered at /api/students/ via the DefaultRouter.
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    search_fields = ["name", "email"]
    ordering_fields = ["name", "email", "id"]

    @action(detail=True, methods=["get"], url_path="courses")
    def student_courses(self, request, pk=None):
        """GET /api/students/<id>/courses/ -> all courses this student is enrolled in."""
        student = self.get_object()
        courses = Course.objects.filter(enrollments__student=student)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseViewSet(viewsets.ModelViewSet):
    """
    Full CRUD ViewSet for Course.

    Provides: list, create, retrieve, update, partial_update, destroy
    Registered at /api/courses/ via the DefaultRouter.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    search_fields = ["title", "code"]
    ordering_fields = ["code", "credits", "id"]

    @action(detail=True, methods=["get"], url_path="students")
    def students(self, request, pk=None):
        """
        Custom action: GET /api/courses/<id>/students/

        Returns only the students enrolled in this specific course, as
        required by the hands-on exercise's Task 2 custom action step.
        """
        course = self.get_object()
        enrolled_students = Student.objects.filter(enrollments__course=course).distinct()
        serializer = CourseStudentsSerializer(enrolled_students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    Full CRUD ViewSet for Enrollment.

    Provides: list, create, retrieve, update, partial_update, destroy
    Registered at /api/enrollments/ via the DefaultRouter.
    Duplicate enrollments are rejected by EnrollmentSerializer.validate().
    """

    queryset = Enrollment.objects.select_related("student", "course").all()
    serializer_class = EnrollmentSerializer
    ordering_fields = ["enrolled_on", "id"]
