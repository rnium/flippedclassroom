from django.urls import path, include
from .views import weeklyDetail, addFiles, downloadFile, edit_post, edit_weekly_view, delete_weekly_view

app_name = "weeklies"

# 'weeklies/' --->

urlpatterns = [
    path('<str:cls_pk>/api/', include('weeklies.api.urls')),
    path('<str:cls_pk>/week/<int:weeknum>', view=weeklyDetail, name='weeklydetail'),
    path('week/<str:pk>/edit', view=edit_weekly_view, name='edit_weekly'),
    path('week/<str:pk>/delete', view=delete_weekly_view, name='delete_weekly'),
    path('<str:weekly_pk>/file/upload', view=addFiles, name='uploadweeklyfiles'),
    path('<str:weekly_pk>/post/<int:pk>/edit', view=edit_post, name='edit_post'),
    path('<str:weekly_pk>/file/<int:pk>/download', view=downloadFile, name='downloadweeklyfile')
]
