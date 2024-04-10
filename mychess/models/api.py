from djoser.views import TokenCreateView
from djoser.conf import settings
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status
from .models import ChessGame
from .serializers import ChessGameSerializer
import random
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


class myclassView(APIView):
    # authentication_classes = [] # disables authentication
    # permission_classes = [] # disables permission
    def get(self, request):
        # return json message
        return Response({"message": "Got some data!"})


# add user_id and rating to the response
# since djoser does not offer them by default
class MyTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        response = super()._action(serializer)
        tokenString = response.data['auth_token']
        tokenObject = settings.TOKEN_MODEL.objects.get(key=tokenString)
        response.data['user_id'] = tokenObject.user.id
        response.data['rating'] = tokenObject.user.rating
        return response


class MyException(PermissionDenied):
    def __init__(self, detail, status_code):
        if detail is not None:
            self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class ChessGameViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = ChessGame.objects.all()
    serializer_class = ChessGameSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        if hasattr(data, "_mutable"):
            _mutable = data._mutable
            data._mutable = True

        game_delete = ChessGame.objects.filter(
            whitePlayer__isnull=True, blackPlayer__isnull=True).exists()
        if game_delete:
            ChessGame.objects.filter(
                whitePlayer__isnull=True, blackPlayer__isnull=True).delete()
            raise MyException(
                detail="Game deleted",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        game_delete = ChessGame.objects.filter(
            whitePlayer__isnull=True).exclude(
                status=ChessGame.PENDING).exists()

        if game_delete:
            ChessGame.objects.filter(whitePlayer__isnull=True).exclude(
                status=ChessGame.PENDING).delete()
            raise MyException(
                detail="Game deleted",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        game_delete = ChessGame.objects.filter(
            blackPlayer__isnull=True).exclude(
                status=ChessGame.PENDING).exists()
        if game_delete:
            ChessGame.objects.filter(blackPlayer__isnull=True).exclude(
                status=ChessGame.PENDING).delete()
            raise MyException(
                detail="Game deleted",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        games = ChessGame.objects.filter(Q(whitePlayer__isnull=True) | Q(
            blackPlayer__isnull=True), status=ChessGame.PENDING)

        if games.exists():
            game = games.first()

            if game.whitePlayer == request.user or\
                    game.blackPlayer == request.user:
                raise MyException(
                    detail="You are already in this game.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            gameID = game.id

            self.kwargs["pk"] = str(gameID)
            result = self.update(request, *args, **kwargs)

        else:
            k = random.randint(0, 1)
            if k == 0:
                data['whitePlayer'] = user.id
            else:
                data['blackPlayer'] = user.id

            data['status'] = ChessGame.PENDING

            if hasattr(data, "_mutable"):
                data._mutable = _mutable

            result = super(ChessGameViewSet, self).create(
                request, *args, **kwargs)

        if hasattr(data, "_mutable"):
            data._mutable = _mutable

        return result

    def update(self, request, *args, **kwargs):
        game = self.get_object()
        user = request.user
        data = request.data

        if game.status != ChessGame.PENDING:
            raise MyException(
                detail="Game is already started.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        kwargs['partial'] = True

        for key in data.keys():
            data[key] = None
        if game.whitePlayer is None:
            data['whitePlayer'] = user.id
        else:
            data['blackPlayer'] = user.id
        data['status'] = ChessGame.ACTIVE

        result = super(ChessGameViewSet, self).update(request, *args, **kwargs)
        return result
