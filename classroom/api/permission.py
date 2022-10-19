from rest_framework.permissions import BasePermission

class IsUserPartOfClassroom(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_teacher = request.user in obj.teachers.all()
        is_student = request.user in obj.student.all()
        print(is_teacher or is_student)
        return is_teacher or is_student