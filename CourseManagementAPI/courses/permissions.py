"""
Custom permission classes for the Course Management API.
"""

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access (GET, HEAD, OPTIONS) to any request.
    Write access (POST, PUT, PATCH, DELETE) is restricted to admin/staff users.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission placeholder: allows read-only access to any
    request, and write access only to the object's related "owner" if the
    object exposes a `student` attribute matching the requesting user.

    Included for extensibility; the API currently uses AllowAny globally.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, "student", None)
        return owner is not None and getattr(owner, "user", None) == request.user
