from django.db import models
from django.contrib.auth.models import AbstractUser
import chess


# Create your models here.
class Player (AbstractUser):
    rating = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.username} ({self.rating})"


class ChessGame (models.Model):
    DEFAULT_BOARD_STATE = chess.Board().fen()

    PENDING = 'pending'
    ACTIVE = 'active'
    FINISHED = 'finished'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (FINISHED, 'Finished')
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default=PENDING)

    # La posición de las piezas en el tablero se almacena en el campo
    # board_state en el formato FEN
    board_state = models.CharField(max_length=128, default=DEFAULT_BOARD_STATE)

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    timeControl = models.CharField(max_length=10, default=10)

    blackPlayer = models.ForeignKey('Player', on_delete=models.SET_NULL,
                                    related_name='black_player', null=True)
    whitePlayer = models.ForeignKey('Player', on_delete=models.SET_NULL,
                                    related_name='white_player', null=True)

    winner = models.ForeignKey('Player', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        white_player = self.whitePlayer if self.whitePlayer else 'unknown'
        black_player = self.blackPlayer if self.blackPlayer else 'unknown'
        return f"GameID=({self.id}) {white_player} vs {black_player}"


class ChessMove (models.Model):
    game = models.ForeignKey(ChessGame, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    move_from = models.CharField(max_length=2)
    move_to = models.CharField(max_length=2)
    promotion = models.CharField(max_length=1, choices=[('q', 'queen'),
                                                        ('r', 'rock'),
                                                        ('n', 'knight'),
                                                        ('b', 'bishop')])

    def __str__(self):
        formatted_str = (
            f"{self.player.username} ({self.player.rating}): "
            f"{self.move_from} -> {self.move_to}"
        )
        return formatted_str

    def save(self, *args, **kwargs):
        if self.game.status != 'active':
            raise Exception('Cannot save move. Game is not active.')

        board = chess.Board(self.game.board_state)

        if self.promotion:
            move = chess.Move.from_uci(
                self.move_from + self.move_to + self.promotion)
        else:
            move = chess.Move.from_uci(self.move_from + self.move_to)

        if move not in list(board.legal_moves):
            print("el movimiento no esta en la lista \n")
            raise ValueError('Invalid move.')

        board.push(move)

        self.game.board_state = board.fen()

        self.game.save()
        super().save(*args, **kwargs)
