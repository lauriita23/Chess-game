<TheChessboard
    :board-config="boardConfig"
    :player-color="playerColor"
    @board-created="(api) => (boardAPI.value = api)"
    @checkmate="handleCheckmate"
    @move="handleMove"
    @stalemate="handleStalemate"
    @draw="handleDraw"
    @promotion="handlePromotion"
    >
</TheChessboard>

