from rest_framework.permissions import BasePermission


class BasePocket(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_pocket == 'Base' or request.user.is_staff


class FullPocket(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_pocket == 'Full' or request.user.is_staff


class NoPocket(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_pocket == 'No':
            return True
        return False
