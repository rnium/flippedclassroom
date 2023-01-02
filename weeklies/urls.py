from django.urls import path, include
app_name = "weeklies"

# 'classroom/<int:cls_pk>/weeklies/' --->

urlpatterns = [
    path('api/', include('weeklies.api.urls')),
]
