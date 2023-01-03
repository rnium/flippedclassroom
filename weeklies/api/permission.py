from rest_framework.permissions import BasePermission


class IsUserTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_teacher = request.user in obj.classroom.teachers.all()
        return is_teacher