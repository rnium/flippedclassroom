from django.urls import path
from weeklies.api.views import (update_weekly, createWeekly, add_tutorial, create_post, delete_weekly,
                                weekly_performance_api)

# 'classroom/<int:cls_pk>/weeklies/api/' --->

urlpatterns = [
    path('create', createWeekly, name='create_weekly'),
    path('<str:pk>/update', update_weekly, name='update_weekly'),
    path('<str:pk>/delete', delete_weekly, name='delete_weekly'),
    path('<str:pk>/tutorial/add', add_tutorial, name='add_tutorial'),
    path('<str:pk>/post/add', create_post, name='create_post'),
    path('<str:pk>/performance', weekly_performance_api, name='weekly_performance_api'),
]
