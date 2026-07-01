"""
Test suite for the Course Management API.

Covers:
    - Model / serializer validation (duplicate email, duplicate course code,
      duplicate enrollment, missing fields, invalid credits)
    - CRUD operations for all four ViewSets
    - Custom /api/courses/<id>/students/ action
    - 404 handling for invalid IDs
    - 400 handling for invalid payloads
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Department, Student, Course, Enrollment
from courses.serializers import (
    DepartmentSerializer,
    StudentSerializer,
    CourseSerializer,
    EnrollmentSerializer,
)


class DepartmentModelAndAPITests(APITestCase):
    """Tests for the Department model, serializer, and CRUD endpoints."""

    def setUp(self):
        self.department = Department.objects.create(
            name="Computer Science", description="Department of Computer Science"
        )
        self.list_url = reverse("courses:department-list")

    def test_department_str(self):
        self.assertEqual(str(self.department), "Computer Science")

    def test_list_departments(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_department_success(self):
        payload = {"name": "Mathematics", "description": "Department of Mathematics"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 2)

    def test_create_department_duplicate_name_fails(self):
        payload = {"name": "Computer Science", "description": "Duplicate"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_department_missing_name_fails(self):
        response = self.client.post(self.list_url, {"description": "No name"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_department_not_found(self):
        url = reverse("courses:department-detail", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_department(self):
        url = reverse("courses:department-detail", args=[self.department.id])
        response = self.client.put(
            url, {"name": "CS Updated", "description": "Updated"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.name, "CS Updated")

    def test_delete_department(self):
        url = reverse("courses:department-detail", args=[self.department.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.count(), 0)


class StudentModelAndAPITests(APITestCase):
    """Tests for the Student model, serializer, and CRUD endpoints."""

    def setUp(self):
        self.department = Department.objects.create(name="Physics", description="Physics dept")
        self.student = Student.objects.create(
            name="Alice Johnson",
            email="alice@example.com",
            phone="1234567890",
            department=self.department,
        )
        self.list_url = reverse("courses:student-list")

    def test_create_student_success(self):
        payload = {
            "name": "Bob Smith",
            "email": "bob@example.com",
            "phone": "9876543210",
            "department": self.department.id,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_student_duplicate_email_fails(self):
        payload = {
            "name": "Alice Clone",
            "email": "alice@example.com",
            "phone": "1112223333",
            "department": self.department.id,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data["details"] if "details" in response.data else response.data)

    def test_create_student_missing_fields_fails(self):
        response = self.client.post(self.list_url, {"name": "No Email"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_invalid_department_fails(self):
        payload = {
            "name": "Ghost Student",
            "email": "ghost@example.com",
            "phone": "1234567890",
            "department": 9999,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_student_not_found(self):
        url = reverse("courses:student-detail", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CourseModelAndAPITests(APITestCase):
    """Tests for the Course model, serializer, CRUD endpoints and custom action."""

    def setUp(self):
        self.department = Department.objects.create(name="Computer Science", description="CS dept")
        self.course = Course.objects.create(
            title="Intro to Programming", code="CS101", credits=4, department=self.department
        )
        self.list_url = reverse("courses:course-list")

    def test_create_course_success(self):
        payload = {
            "title": "Data Structures",
            "code": "CS201",
            "credits": 4,
            "department": self.department.id,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_duplicate_code_fails(self):
        payload = {
            "title": "Intro Duplicate",
            "code": "CS101",
            "credits": 3,
            "department": self.department.id,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_course_invalid_credits_fails(self):
        payload = {
            "title": "Overloaded Course",
            "code": "CS999",
            "credits": 99,
            "department": self.department.id,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_course(self):
        url = reverse("courses:course-detail", args=[self.course.id])
        payload = {
            "title": "Intro to Programming Updated",
            "code": "CS101",
            "credits": 3,
            "department": self.department.id,
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        url = reverse("courses:course-detail", args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_course_students_custom_action(self):
        student = Student.objects.create(
            name="Charlie Brown",
            email="charlie@example.com",
            phone="5551234567",
            department=self.department,
        )
        Enrollment.objects.create(student=student, course=self.course)

        url = reverse("courses:course-students", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "charlie@example.com")

    def test_course_students_custom_action_empty(self):
        url = reverse("courses:course-students", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_course_students_invalid_course_404(self):
        url = reverse("courses:course-students", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EnrollmentModelAndAPITests(APITestCase):
    """Tests for the Enrollment model, serializer, and duplicate prevention."""

    def setUp(self):
        self.department = Department.objects.create(name="Biology", description="Bio dept")
        self.student = Student.objects.create(
            name="Dana White",
            email="dana@example.com",
            phone="1231231234",
            department=self.department,
        )
        self.course = Course.objects.create(
            title="Genetics 101", code="BIO101", credits=3, department=self.department
        )
        self.list_url = reverse("courses:enrollment-list")

    def test_create_enrollment_success(self):
        payload = {"student": self.student.id, "course": self.course.id}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_duplicate_enrollment_fails(self):
        Enrollment.objects.create(student=self.student, course=self.course)
        payload = {"student": self.student.id, "course": self.course.id}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_enrollment_missing_fields_fails(self):
        response = self.client.post(self.list_url, {"student": self.student.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_enrollment_invalid_ids_fails(self):
        payload = {"student": 9999, "course": 9999}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_enrollment(self):
        enrollment = Enrollment.objects.create(student=self.student, course=self.course)
        url = reverse("courses:enrollment-detail", args=[enrollment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SerializerUnitTests(APITestCase):
    """Direct unit tests for serializer validation logic."""

    def setUp(self):
        self.department = Department.objects.create(name="Chemistry", description="Chem dept")

    def test_department_serializer_valid(self):
        serializer = DepartmentSerializer(data={"name": "New Dept", "description": "desc"})
        self.assertTrue(serializer.is_valid())

    def test_student_serializer_invalid_email(self):
        serializer = StudentSerializer(
            data={
                "name": "Test User",
                "email": "not-an-email",
                "phone": "1234567890",
                "department": self.department.id,
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_course_serializer_invalid_code_format(self):
        serializer = CourseSerializer(
            data={
                "title": "Bad Code Course",
                "code": "invalidcode123",
                "credits": 3,
                "department": self.department.id,
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("code", serializer.errors)

    def test_enrollment_serializer_duplicate(self):
        student = Student.objects.create(
            name="Eve Adams",
            email="eve@example.com",
            phone="1231231234",
            department=self.department,
        )
        course = Course.objects.create(
            title="Organic Chemistry", code="CHEM201", credits=4, department=self.department
        )
        Enrollment.objects.create(student=student, course=course)

        serializer = EnrollmentSerializer(data={"student": student.id, "course": course.id})
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)


class FunctionBasedViewTests(APITestCase):
    """Tests for the Part 1 function-based Department demo views."""

    def setUp(self):
        self.department = Department.objects.create(name="History", description="History dept")

    def test_fbv_department_list_get(self):
        url = reverse("courses:fbv-department-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fbv_department_list_post(self):
        url = reverse("courses:fbv-department-list")
        response = self.client.post(url, {"name": "Art", "description": "Art dept"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fbv_department_detail_get(self):
        url = reverse("courses:fbv-department-detail", args=[self.department.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fbv_department_detail_not_found(self):
        url = reverse("courses:fbv-department-detail", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fbv_department_detail_delete(self):
        url = reverse("courses:fbv-department-detail", args=[self.department.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ClassBasedViewTests(APITestCase):
    """Tests for the Part 2 class-based Student demo views."""

    def setUp(self):
        self.department = Department.objects.create(name="Economics", description="Econ dept")

    def test_cbv_student_apiview_get(self):
        url = reverse("courses:cbv-student-apiview")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cbv_student_apiview_post(self):
        url = reverse("courses:cbv-student-apiview")
        payload = {
            "name": "Frank Miller",
            "email": "frank@example.com",
            "phone": "1231231234",
            "department": self.department.id,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cbv_generic_list_create(self):
        url = reverse("courses:cbv-student-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cbv_generic_detail_not_found(self):
        url = reverse("courses:cbv-student-detail", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
