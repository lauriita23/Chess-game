from models.models import ChessGame
from rest_framework.authtoken.models import Token
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
# from django.contrib.auth.models import User
from models.consumers import ChessConsumer
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.urls import path, reverse
from channels.routing import URLRouter
from channels.testing import ChannelsLiveServerTestCase

# you may modify the following lines
URL = '/api/v1/games/'
# do not modify the code below

User = get_user_model()


class ChessGameAPITest2(TestCase):

    def setUp(self):
        ChessGame.objects.all().delete()
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1', password='testpassword')
        self.user2 = User.objects.create_user(
            username='user2', password='testpassword')

    def test_000_check_current_player_in_game(self):
        game = ChessGame.objects.create(whitePlayer=self.user1)
        game.save()
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'{URL}', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("response data ", response.data)
        self.assertEqual(response.data['detail'],
                         "You are already in this game.")

    def test_002_delete_game_when_players_are_null(self):
        game = ChessGame.objects.create(whitePlayer=None, blackPlayer=None)
        game.save()
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(URL, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Game deleted")
        self.assertFalse(ChessGame.objects.filter(id=game.id).exists())

    def test_003_delete_game_white_player_null_status_not_pending(self):
        game = ChessGame.objects.create(whitePlayer=None,
                                        status=ChessGame.ACTIVE)
        game.save()
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(URL, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Game deleted")
        self.assertFalse(ChessGame.objects.filter(id=game.id).exists())

    @patch('random.randint', return_value=0)
    def test_004_create_game_white_player(self, randint_mock):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(URL, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        game = ChessGame.objects.first()
        self.assertEqual(game.whitePlayer, self.user1)

    @patch('random.randint', return_value=0)
    def test_create_game_white_player(self, randint_mock):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(URL, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        game = ChessGame.objects.create(whitePlayer=None,
                                        status=ChessGame.ACTIVE)
        response = self.client.post(URL, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Game deleted")
        game.delete()
        game = ChessGame.objects.create(blackPlayer=None,
                                        status=ChessGame.ACTIVE)
        response = self.client.post(URL, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Game deleted")


class MyClassViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token_url = '/api/v1/myclassView/'

    def test_001_myclassView(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('myclassView')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Got some data!"})


class ChessGameAPITestUpdate(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.game = ChessGame.objects.create(status='pending')

    def test_001_update_game_status(self):
        url = reverse('chessgame-detail', kwargs={'pk': self.game.pk})
        data = {'status': 'active'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.game.refresh_from_db()
        self.assertEqual(self.game.status, 'active')


class ChessConsumerTest2(TestCase):
    def setUp(self):
        self.white_user = User.objects.create_user(
            username='white', password='testpassword')
        self.black_user = User.objects.create_user(
            username='black', password='testpassword')
        self.white_token, _ = Token.objects.get_or_create(
            user=self.white_user)
        self.black_token, _ = Token.objects.get_or_create(
            user=self.black_user)
        self.white_token.save()
        self.black_token.save()

        self.white_token_key = self.white_token.key
        self.black_token_key = self.black_token.key

        self.game = ChessGame.objects.create(
            whitePlayer=self.white_user)
        self.game.save()
        self.game2 = ChessGame.objects.create(
            whitePlayer=self.white_user,
            blackPlayer=self.black_user,
            status='active')
        self.game2.save()
        self.consumer = ChessConsumer()

    def test_001_get_game_returns_minus_one_when_game_does_not_exist(self):
        self.assertEqual(self.consumer.getGame(999), -1)

    def test_get_game_exists(self):
        result = self.consumer.getGame(self.game.id)
        self.assertEqual(result, self.game)

    def test_get_game_not_exists(self):
        result = self.consumer.getGame(-1)
        self.assertEqual(result, -1)

    def test_get_game_null_id(self):
        result = self.consumer.getGame(None)
        self.assertEqual(result, -1)

    def test_get_player_not_exists(self):
        self.assertEqual(self.consumer.getPlayer(999), -1)


application = URLRouter([
    path("ws/play/<int:gameID>/", ChessConsumer.as_asgi()),
])


class ChessConsumerTests1(ChannelsLiveServerTestCase):
    """Test the chess consumer"""
    def setUp(self):
        self.white_user = User.objects.create_user(
            username='white', password='testpassword')
        self.black_user = User.objects.create_user(
            username='black', password='testpassword')
        self.white_token, _ = Token.objects.get_or_create(
            user=self.white_user)
        self.black_token, _ = Token.objects.get_or_create(
            user=self.black_user)
        self.white_token.save()
        self.black_token.save()

        self.white_token_key = self.white_token.key
        self.black_token_key = self.black_token.key

        self.game = ChessGame.objects.create(
            whitePlayer=self.white_user)
        self.game.save()  # single player
        self.game2 = ChessGame.objects.create(
            whitePlayer=self.white_user,
            blackPlayer=self.black_user,
            status='active')
        self.game2.save()  # two players

    async def connect_and_verify(self, gameID, token_key):
        communicator = WebsocketCommunicator(
            application, f"/ws/play/{gameID}/?{token_key}")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        response = await communicator.receive_json_from()
        return response, communicator

    async def test_chess_consumer_receive_invalid_type(self):
        """Test receive method with invalid type."""
        self.gameID = self.game2.id

        response, communicator = await self.connect_and_verify(
            self.gameID,
            self.white_token_key)
        self.assertEqual(response["type"], "game")
        self.assertEqual(response["message"], "OK")

        await communicator.send_json_to({
            "type": "invalid_type",
            "data": "some_data",
        })

        try:
            response = await communicator.receive_json_from()
        except Exception as e:
            print("Exception:", e)

        self.assertEqual(response.get("type"), "error")
        self.assertEqual(response.get("message"), "Error: invalid type")

        await communicator.disconnect()

    async def test_chess_consumer_receive_invalid_player_id(self):
        """Test receive method with invalid player_id."""
        self.gameID = self.game2.id

        response, communicator = await self.connect_and_verify(
            self.gameID,
            self.white_token_key)
        self.assertEqual(response["type"], "game")
        self.assertEqual(response["message"], "OK")

        await communicator.send_json_to({
            "type": "move",
            "from": "e2",
            "to": "e4",
            "playerID": "-1",
            "promotion": "q",
        })

        response = await communicator.receive_json_from()

        self.assertEqual(response.get("type"), "error")
        self.assertEqual(
            response.get("message"), f"Invalid game with id {self.gameID}")

        await communicator.disconnect()

    async def test_user_not_in_game_single_player(self):
        """Test userNotInGame function with only one player in the game."""
        self.gameID = self.game.id
        response, communicator = await self.connect_and_verify(
            self.gameID,
            self.white_token_key)
        self.assertEqual(response["type"], "game")
        self.assertEqual(response["message"], "OK")

        # Disconnect and connect with another user
        await communicator.disconnect()
        response, communicator = await self.connect_and_verify(
            self.gameID,
            self.black_token_key)
        self.assertEqual(response["type"], "error")
        self.assertEqual(
            response["message"], f"Invalid game with id {self.gameID}")

        await communicator.disconnect()
