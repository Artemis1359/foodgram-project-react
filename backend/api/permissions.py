from rest_framework import permissions


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """Доступ только пользователея с ролью 'Admin', либо только чтение."""

    def has_object_permission(self, request, view, obj):
        return request.method == 'GET' or (request.user.is_authenticated
                                           and (request.user.is_staff
                                                or request.user == obj.author))
