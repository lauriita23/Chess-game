import json
import chess
from .models import ChessGame, Player, ChessMove
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async


class ChessConsumer(AsyncWebsocketConsumer):
    def getUserId(self, token):
        tokens = Token.objects.filter(key=token)
        if tokens.exists():
            return tokens[0].user_id
        return -1

    def getGame(self, game_id):
        if self.checkGameExist(game_id) is False:
            return -1
        game = ChessGame.objects.get(id=game_id)
        if game is not None:
            return game
        return -1

    def getPlayer(self, player_id):
        if Player.objects.filter(id=player_id).exists() is False:
            return -1
        player = Player.objects.get(id=player_id)
        if player.exists():
            return player
        print("Player does not exist")
        return -1

    def checkGameExist(self, game_id):
        return ChessGame.objects.filter(id=game_id).exists()

    def userNotInGame(self, game_id, user_id):
        game = ChessGame.objects.get(id=game_id)
        if game.whitePlayer is not None and game.blackPlayer is not None:
            if (game.whitePlayer.id == user_id or
                    game.blackPlayer.id == user_id):
                return True
        elif game.whitePlayer is not None:
            if game.whitePlayer.id == user_id:
                return True
        elif game.blackPlayer is not None:
            if game.blackPlayer.id == user_id:
                return True

        return False

    def salvarMovimiento(self, game_id, player_id, _from, to, promotion):
        game = ChessGame.objects.get(id=game_id)
        player = Player.objects.get(id=player_id)
        try:
            chess_move = ChessMove(game=game, player=player, move_from=_from,
                                   move_to=to, promotion=promotion)
            chess_move.save()
        except Exception as e:
            print("Exception: ", e)
            return False

        board_state = game.board_state
        board = chess.Board(board_state)
        if board.is_checkmate():
            game.winner = player
            game.status = ChessGame.FINISHED

        return True

    def validGame(self, game_id):
        game = ChessGame.objects.get(id=game_id)
        if game.status == 'finished':
            return False
        return True

    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['gameID']
        self.room_group_name = str(self.game_id)
        token_name = (
            self.scope['query_string'].decode()
            if 'query_string' in self.scope
            else None
        )

        game_exist = await database_sync_to_async(
            self.checkGameExist)(self.game_id)
        game_new = await database_sync_to_async(self.getGame)(self.game_id)

        await self.accept()

        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)

        if game_exist is False:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_cb',
                    'type_': 'error',
                    'message': f"Invalid game with id {self.game_id}",
                    'status': 'None',
                    'playerID': 'None'
                })
            await self.disconnect(self.room_group_name)
            return

        self.user_id = await database_sync_to_async(self.getUserId)(token_name)

        if self.user_id == -1:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_cb',
                    'type_': 'error',
                    'message': 'Invalid token. Connection not authorized.',
                    'status': 'None',
                    'playerID': 'None'
                })
            await self.disconnect(self.room_group_name)
            return

        result = await database_sync_to_async(self.userNotInGame)(
            self.game_id, self.user_id)
        if result is False:
            await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                            'type': 'game_cb',
                            'type_': 'error',
                            'message': f"Invalid game with id {self.game_id}",
                            'status': 'None',
                            'playerID': 'None'
                    })
            await self.disconnect(self.room_group_name)
            return
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_cb',
                'type_': 'game',
                'message': 'OK',
                'status': game_new.status,
                'playerID': self.user_id
            })

        return True

    async def receive(self, text_data):
        data = json.loads(text_data)
        type = data['type']

        if type == 'move':
            _from = data['from']
            to = data['to']
            playerID = data['playerID']
            promotion = data['promotion']

            game_valid = await database_sync_to_async(
                self.validGame)(self.game_id)
            if playerID != self.user_id:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                            'type': 'move_cb',
                            'type_': 'error',
                            'message': f"Invalid game with id {self.game_id}",
                    })
                return
            if game_valid is False:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                            'type': 'move_cb',
                            'type_': 'error',
                            'message':
                            "Error: invalid move (game is not active)",
                    })
                return
            save = await database_sync_to_async(self.salvarMovimiento)(
                self.game_id, playerID, _from, to, promotion)
            if save is False:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                            'type': 'move_cb',
                            'type_': 'error',
                            'message': f"Error: invalid move {_from}{to}",
                    })
                return

            # Llama a la función move_cb solo después de guardar el movimiento
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'move_cb',
                    'type_': 'move',
                    'from': _from,
                    'to': to,
                    'playerID': playerID,
                    'promotion': promotion
                })
            return True
        
        await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                            'type': 'move_cb',
                            'type_': 'error',
                            'message':
                            "Error: invalid type",
                    })
        return

    async def game_cb(self, event):
        message = event['message']
        type = event['type_']
        status = event['status']
        playerID = event['playerID']
        await self.send(text_data=json.dumps({
            'type': type,
            'message': message,
            'status': status,
            'playerID': playerID
        }))

    async def move_cb(self, event):
        if event['type_'] != 'move':
            data = {
                    'type': event['type_'],
                    'message': event['message'],
                }
        else:
            data = {
                'type': event['type_'],
                'from': event['from'],
                'to': event['to'],
                'playerID': event['playerID'],
                'promotion': event['promotion'],
            }
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
