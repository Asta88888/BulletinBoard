from rest_framework.permissions import BasePermission

from users.models import User


class IsAdmin(BasePermission):
    """
    Проверка принадлежности пользователя к группе администратора.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ADMIN


class IsSelf(BasePermission):
    """
    Проверка, что объект пользователя — это текущий пользователь.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminOrSelf(BasePermission):
    """
    Разрешает редактировать/удалять только администратору или самому пользователю.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.ADMIN or obj == request.user


class IsOwner(BasePermission):
    """
    Проверка принадлежности пользователя к владельцам объекта.
    """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False
