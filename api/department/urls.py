from django.urls import path

from api.student.views import StudentLoginAPIView

urlpatterns = [
    path("login/", StudentLoginAPIView.as_view()),
]
