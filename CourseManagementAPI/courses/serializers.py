"""
Serializers for the Course Management API.

Each ModelSerializer includes explicit validation for uniqueness constraints
(course code, student email) and duplicate enrollment prevention, with
clear, descriptive error messages.
"""

from rest_framework import serializers

from courses.models import Department, Student, Course, Enrollment


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for the Department model."""

    student_count = serializers.SerializerMethodField(read_only=True)
    course_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "description", "student_count", "course_count"]

    def get_student_count(self, obj):
        return obj.students.count()

    def get_course_count(self, obj):
        return obj.courses.count()

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Department name cannot be blank.")
        qs = Department.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A department with this name already exists.")
        return value


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for the Student model."""

    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Student
        fields = ["id", "name", "email", "phone", "department", "department_name"]

    def validate_email(self, value):
        value = value.strip().lower()
        qs = Student.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A student with this email already exists.")
        return value

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Student name cannot be blank.")
        return value


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for the Course model."""

    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "code", "credits", "department", "department_name"]

    def validate_code(self, value):
        value = value.strip().upper()
        qs = Course.objects.filter(code__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A course with this code already exists.")
        return value

    def validate_credits(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Credits must be between 1 and 10.")
        return value

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Course title cannot be blank.")
        return value


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for the Enrollment model. Prevents duplicate enrollments."""

    student_name = serializers.CharField(source="student.name", read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)
    course_code = serializers.CharField(source="course.code", read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "course",
            "enrolled_on",
            "student_name",
            "course_title",
            "course_code",
        ]
        read_only_fields = ["enrolled_on"]

    def validate(self, attrs):
        student = attrs.get("student", getattr(self.instance, "student", None))
        course = attrs.get("course", getattr(self.instance, "course", None))

        qs = Enrollment.objects.filter(student=student, course=course)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["This student is already enrolled in this course."]}
            )
        return attrs


class CourseStudentsSerializer(serializers.ModelSerializer):
    """Lightweight serializer used by the custom /courses/<id>/students/ action."""

    class Meta:
        model = Student
        fields = ["id", "name", "email", "phone", "department"]
