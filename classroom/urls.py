from django.urls import path, include
from .views import *
app_name = 'classroom'

urlpatterns = [
    path('', ClassesDashboard.as_view(), name="homepage"),
    path('classroom/api/', include("classroom.api.urls")),
    path('classroom/<str:pk>', ClassroomDetail.as_view(), name="classroom_detail"),
    path('classroom/join/<str:pk>', join_classroom, name="join_classroom"),
]
   