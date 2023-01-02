from rest_framework.permissions import BasePermission

class IsUserPartOfClassroom(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_teacher = request.user in obj.teachers.all()
        is_student = request.user in obj.students.all()
        return is_teacher or is_student

class IsUserTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_teacher = request.user in obj.teachers.all()
        return is_teacher