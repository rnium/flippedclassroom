from django.urls import path
from . import views

urlpatterns = [
    path('newclassroom', views.create_classroom, name="create_classroom_api"),
    path('join', views.classroom_join_api, name="classroom_join_api"),
    path('<str:pk>/changecode', views.change_join_code, name="change_join_code"),
    path('<str:pk>/posts', views.ClassroomPostsView.as_view(), name="classroom_posts"),
    path('<str:pk>/update', views.UpdateClassroomAV.as_view(), name="update_classroom"),
    path('<str:pk>/delete', views.delete_classroom_api, name="delete_classroom_api"),
    path('<str:pk>/congratulate', views.congratulate_user, name="congratulate_user"),
    path('<str:pk>/update/banner', views.set_banner, name="set_banner"),
    path('<str:pk>/update/banner/todefault', views.set_banner_to_default, name="set_banner_to_default"),
    path('<str:pk>/addteacher', views.add_teacher, name="add_teacher"),
    path('<str:cls_pk>/assessments/update', views.update_assessments, name="update_assessments"),
    path('<str:cls_pk>/assessments/delete', views.delete_assessment_meta, name="delete_assessment_meta"),
    path('<str:cls_pk>/ranking', views.get_ranking_api, name="get_ranking_api"),
    # path('<str:pk>/edit', views.update_classroom_info, name="update_classroom"),
    path('<str:pk>/removeuser', views.remove_user_from_classroom, name="remove_user_from_classroom"),
    path('post/<str:pk>/postcomment', views.post_comment, name="post_comment"),
    path('post/<str:pk>/update', views.update_post_des_and_rm_files, name="update_post_des_and_rm_files"),
    path('post/<str:pk>/delete', views.delete_post, name="delete_post_api"),
]
   