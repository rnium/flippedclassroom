from rest_framework.permissions import BasePermission

class IsUserTeacherOfClassroom(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_teacher = request.user in obj.weekly.classroom.teachers.all()
        return is_teacher