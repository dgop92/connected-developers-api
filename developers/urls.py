from django.urls import path
from developers import views

realtime_name = "realtime"
register_name = "register"

urlpatterns = [
    path(
        "realtime/<str:dev1>/<str:dev2>", 
        views.realtime_view, name=realtime_name
    ),

    path(
        "register/<str:dev1>/<str:dev2>", 
        views.register_view, name=register_name
    ),
]