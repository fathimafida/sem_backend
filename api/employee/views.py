from rest_framework import serializers, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Check if the email exists in the Employee model
        try:
            employee = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            raise serializers.ValidationError({"message": "Invalid email"})

        # Check if the employee is active
        if not employee.is_active:
            raise serializers.ValidationError({"message": "Inactive employee account"})

        # Authenticate the employee using the email and password
        user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )
        if user is None:
            raise serializers.ValidationError({"message": "Invalid credentials"})

        attrs["employee"] = employee
        return attrs


class EmployeeLoginAPIView(APIView):
    serializer_class = EmployeeLoginSerializer

    # @csrf_exempt
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            errors = e.get_full_details()
            error_messages = []
            for field, field_errors in errors.items():
                for error in field_errors:
                    error_messages.append(error["message"])
            return Response(
                {"message": error_messages}, status=status.HTTP_400_BAD_REQUEST
            )

        employee = serializer.validated_data["employee"]
        serialized_employee = EmployeeSerializer(employee)

        return Response(serialized_employee.data, status=status.HTTP_200_OK)


# Updata Employee


class EmployeeRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
