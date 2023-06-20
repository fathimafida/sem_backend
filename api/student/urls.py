from django.urls import path

from api.student.views import StudentLoginAPIView, StudentRetrieveUpdateAPIView

urlpatterns = [
    path("login/", StudentLoginAPIView.as_view()),
    path("<int:pk>/", StudentRetrieveUpdateAPIView.as_view()),
]
