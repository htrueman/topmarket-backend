from rest_framework.permissions import BasePermission


class BasePocket(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_pocket == 'BASE' or request.user.is_staff


class FullPocket(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.user_pocket == 'FULL' or request.user.is_staff)


class NoPocket(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_pocket == 'NO':
            return True
        return False


class IsContractor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.role == 'CONTRACTOR' or request.user.is_staff):
            return True
        return False


class IsPartner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.role == 'PARTNER' or request.user.is_staff):
            return True
        return False


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
