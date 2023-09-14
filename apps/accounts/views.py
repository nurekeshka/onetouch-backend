from .constants import AccountsSuccessMessages
from .constants import AccountsErrorMessages
from .response import BadRequestException
from .response import SuccessCreatedResponse
from rest_framework.views import APIView
from .serializers import UserSerializer
from .serializers import TokenSerializer
from . import utils


class AccountsView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.POST, many=False)

        if not serializer.is_valid():
            return BadRequestException(AccountsErrorMessages.invalid_info.value, serializer.errors)

        user = serializer.create(serializer.validated_data)
        user.save()

        token = utils.get_user_token(user)
        
        serializer = TokenSerializer(instance=token)

        return SuccessCreatedResponse(AccountsSuccessMessages.created.value, serializer.data)
