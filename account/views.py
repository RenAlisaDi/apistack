from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import RegisterSerializer


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                "Successfully registered!", 201
            )


class ActivationView(APIView):

    def get(self, request, email, activation_code):
        user = CustomUser.objects.filter(
            email=email,
            activation_code=activation_code
        ).first()
        msg_ = ("User does not exist", "Activated!")
        if not user:
            return Response(msg_[0], 400)
        user.activation_code = ''
        user_is_active = True
        user.save()
        return Response(msg_[-1], 200)