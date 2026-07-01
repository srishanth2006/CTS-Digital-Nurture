"""
Django admin configuration for the Course Management API models.
"""

from django.contrib import admin

from courses.models import Department, Student, Course, Enrollment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "student_count", "course_count")
    search_fields = ("name", "description")
    ordering = ("name",)
    list_filter = ()

    @admin.display(description="Students")
    def student_count(self, obj):
        return obj.students.count()

    @admin.display(description="Courses")
    def course_count(self, obj):
        return obj.courses.count()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "department")
    search_fields = ("name", "email", "phone")
    list_filter = ("department",)
    ordering = ("name",)
    autocomplete_fields = ("department",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "title", "credits", "department")
    search_fields = ("code", "title")
    list_filter = ("department", "credits")
    ordering = ("code",)
    autocomplete_fields = ("department",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "course", "enrolled_on")
    search_fields = ("student__name", "student__email", "course__code", "course__title")
    list_filter = ("course", "enrolled_on")
    ordering = ("-enrolled_on",)
    autocomplete_fields = ("student", "course")
