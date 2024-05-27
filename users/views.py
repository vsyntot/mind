from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import LoginSerializer, UsersListSerializer, UsersDetailSerializer
from .serializers import RegistrationSerializer


class RegistrationAPIView(APIView):
    """
    Registers a new user.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
                'is_active': serializer.validated_data.get('is_active', None),
                'role': serializer.validated_data.get('role', None)
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UsersListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersListSerializer
    queryset = User.objects.all()


class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersDetailSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.get(pk=kwargs.get("pk"))
        if data.get('project_list', None):
            new_list = [int(x) for x in data.get('project_list', None).split(',')]
            user.project_list.set(new_list)
        if data.get('username', None):
            user.username = data.get("username")
        if data.get('role', None):
            user.role = data.get("role")
        if data.get('is_staff', None):
            user.is_staff = data.get("is_staff")
        if data.get('is_active', None):
            user.is_active = data.get("is_active")
        if data.get('email', None):
            user.email = data.get("email")
        user.save()
        return self.get(request, *args, **kwargs)
