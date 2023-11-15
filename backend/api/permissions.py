from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Доступ только для автора, либо только чтение."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.recipes == obj.author
