from rest_framework import serializers, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class StudentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Check if the email exists in the Student model
        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            raise serializers.ValidationError({"message": "Invalid email"})

        # Check if the student is active
        if not student.is_active:
            raise serializers.ValidationError({"message": "Inactive student account"})

        # Authenticate the student using the email and password
        user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )
        if user is None:
            raise serializers.ValidationError({"message": "Invalid credentials"})

        attrs["student"] = student
        return attrs


class StudentLoginAPIView(APIView):
    serializer_class = StudentLoginSerializer

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

        student = serializer.validated_data["student"]
        serialized_student = StudentSerializer(student)

        return Response(serialized_student.data, status=status.HTTP_200_OK)


# Updata Student


class StudentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
