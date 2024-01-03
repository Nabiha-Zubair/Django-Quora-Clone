from rest_framework.permissions import BasePermission

class CanDeleteOwnObject(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# class CanDeleteOwnQuestionPermission(BasePermission):
#     def has_permission(self, request, view):
#         question = view.get_object()
#         return request.user == question.user
