from django.contrib import admin

# Register your models here.
from models.models import ChessGame, ChessMove, Player


@admin.register(ChessGame)
class ChessGameAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'start_time', 'end_time', 'timeControl',
                    'whitePlayer', 'blackPlayer', 'winner')
    list_filter = ('status', 'timeControl', 'winner')
    search_fields = ('id', 'status', 'timeControl', 'winner')
    ordering = ('-start_time',)


@admin.register(ChessMove)
class ChessMoveAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'player', 'move_from', 'move_to')
    list_filter = ('player',)
    search_fields = ('id', 'game', 'player', 'move_from', 'move_to')
    ordering = ('-id',)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'rating')
    search_fields = ('username', )
    ordering = ('username',)
