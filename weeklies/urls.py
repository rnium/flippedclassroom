from django.urls import path, include
from .views import weeklyDetail, addFiles, downloadFile

app_name = "weeklies"

# 'classroom/<int:cls_pk>/weeklies/' --->

urlpatterns = [
    path('<str:cls_pk>/api/', include('weeklies.api.urls')),
    path('<str:cls_pk>/week/<int:weeknum>', view=weeklyDetail, name='weeklydetail'),
    path('<str:weekly_pk>/file/upload', view=addFiles, name='uploadweeklyfiles'),
    path('<str:weekly_pk>/file/<int:pk>/download', view=downloadFile, name='downloadweeklyfile')
]
