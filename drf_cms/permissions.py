from rest_framework import permissions

#TODO: Add owner checks when site ownership is integrated to user

class IsOwnerOrReadOnly(permissions.BasePermission):

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True

		return (request.user.is_authenticated and request.user.is_staff)

	def has_object_permission(self, request, view, obj):	
		if request.method in permissions.SAFE_METHODS:
			return True

		return (request.user.is_authenticated and request.user.is_staff)
