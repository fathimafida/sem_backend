from django.urls import path

from api.employee.views import EmployeeLoginAPIView, EmployeeRetrieveUpdateAPIView

urlpatterns = [
    path("login/", EmployeeLoginAPIView.as_view()),
    path('<int:pk>/',EmployeeRetrieveUpdateAPIView.as_view())
]

