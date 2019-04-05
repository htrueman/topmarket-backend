from rest_framework.permissions import BasePermission


class BasePocket(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_pocket == 'BASE' or request.user.is_staff


class FullPocket(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_pocket == 'FULL' or request.user.is_staff


class NoPocket(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_pocket == 'NO':
            return True
        return False
