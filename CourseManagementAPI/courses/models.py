"""
Database models for the Course Management API.

Models:
    Department  - academic department that offers courses and houses students
    Student     - enrolled student, belongs to a department
    Course      - a course offered by a department
    Enrollment  - through-model linking a Student to a Course, prevents duplicates
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from courses.validators import phone_validator, course_code_validator, validate_credits


class Department(models.Model):
    """Represents an academic department, e.g. Computer Science."""

    name = models.CharField(max_length=150, unique=True, help_text="Name of the department.")
    description = models.TextField(blank=True, default="", help_text="Short description of the department.")

    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name


class Student(models.Model):
    """Represents a student enrolled at the institution."""

    name = models.CharField(max_length=150, help_text="Full name of the student.")
    email = models.EmailField(unique=True, help_text="Unique email address of the student.")
    phone = models.CharField(
        max_length=15,
        validators=[phone_validator],
        blank=True,
        default="",
        help_text="Contact phone number.",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="students",
        help_text="Department the student belongs to.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.name} ({self.email})"


class Course(models.Model):
    """Represents a course offered by a department."""

    title = models.CharField(max_length=200, help_text="Title of the course.")
    code = models.CharField(
        max_length=10,
        unique=True,
        validators=[course_code_validator],
        help_text="Unique course code, e.g. CS101.",
    )
    credits = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10), validate_credits],
        help_text="Number of academic credits (1-10).",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="courses",
        help_text="Department that offers this course.",
    )

    class Meta:
        ordering = ["code"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.code} - {self.title}"


class Enrollment(models.Model):
    """
    Represents the enrollment of a Student into a Course.

    A unique_together constraint on (student, course) prevents duplicate
    enrollments at the database level, complementing serializer-level validation.
    """

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
        help_text="Student being enrolled.",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
        help_text="Course the student is enrolling in.",
    )
    enrolled_on = models.DateTimeField(auto_now_add=True, help_text="Timestamp of enrollment.")

    class Meta:
        ordering = ["-enrolled_on"]
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="unique_student_course_enrollment")
        ]

    def __str__(self):
        return f"{self.student.name} -> {self.course.code}"
