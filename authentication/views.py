from rest_framework.views import APIView
from authentication.serializers import SignupSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)