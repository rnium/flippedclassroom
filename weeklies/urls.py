from django.urls import path, include

app_name = "weeklies"

# 'classroom/<int:cls_pk>/weeklies/' --->

urlpatterns = [
    path('<str:cls_pk>/api/', include('weeklies.api.urls')),
]
