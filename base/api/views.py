from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from platy.models import Friends
from api.serializers import UserSerializer, FriendSerializer


@api_view(['GET'])
def get_users_api_view(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)






