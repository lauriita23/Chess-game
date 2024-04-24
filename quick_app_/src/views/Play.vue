<template>
    <TheChessboard
        :board-config="boardConfig"
        :player-color="playerColor"
        @board-created="(api) => (boardAPI.value = api)"
        @checkmate="handleCheckmate"
        @move="handleMove"
        @stalemate="handleStalemate"
        @draw="handleDraw"
        @promotion="handlePromotion" 
        @check="handleCheck"
        reactive-config
        >
    </TheChessboard>
    <table>
        <tr v-for="(move, index) in moves" :key="index">
            <td>{{ move.white }}</td>
            <td>{{ move.black }}</td>
        </tr>
    </table>
    <div>
    <button @click="boardConfig.coordinates = !boardConfig.coordinates">
      Toggle coordinates
    </button>
    <button @click="boardConfig.viewOnly = !boardConfig.viewOnly">
      Toggle view only
    </button>
    <button
      @click="boardConfig.animation.enabled = !boardConfig.animation.enabled"
    >
      Toggle animations
    </button>
    <button
      @click="boardConfig.draggable.enabled = !boardConfig.draggable.enabled"
    >
      Toggle draggable
    </button>
  </div>
</template>


<script setup>
import { reactive } from 'vue';
import { onMounted } from 'vue';
import { BoardApi, MoveEvent, PromotionEvent, TheChessboard, Color, Square, PieceSymbol } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';

const boardConfig = reactive({
  coordinates: true,
  viewOnly: false,
  animation: { enabled: true },
  draggable: { enabled: true },
  trustAllEvents: true, 
});

let boardApi;

// Client will only be able to play white pieces.
const playerColor = 'white';

// Recieve move from socket/server/etc here.
function onRecieveMove(move) {
  boardApi?.move(move);
}

const emit = defineEmits<{
  (e: 'boardCreated', boardApi: BoardApi): void; // emits boardAPI
  (e: 'checkmate', isMated: PieceColor): void; // emits the color of the mated player
  (e: 'stalemate'): void; // just emits stalemate, the value is not interesting
  (e: 'draw'): void; // same for draw
  (e: 'check', isInCheck: PieceColor): void; // emits color who is in check
  (e: 'promotion', promotion: PromotionEvent): void; // emits information about the promotion
  (e: 'move', move: MoveEvent): void; // emits information about the move
}>();

export type PieceColor = 'white' | 'black';

export interface PromotionEvent {
  color: 'white' | 'black';
  sanMove: string;
  promotedTo: 'Q' | 'B' | 'R' | 'N';
}

function handleCheck(isInCheck) {
  alert(`${isInCheck} is in Check`);
}

function handleMove(move) {
  console.log(move);
}


function handleCheckmate(isMated) {
  alert(`${isMated} is mated`);
}

function handlePromotion(promotion) {
  console.log(promotion);
}

function handleStalemate() {
  alert('Stalemate');
}


function handleDraw() {
  alert('Draw');
}

onMounted(() => {
  console.log(boardApi?.getBoardPosition());
});


type MoveEvent = {
  color: Color;
  from: Square;
  to: Square;
  piece: PieceSymbol;
  captured?: PieceSymbol;
  promotion?: PieceSymbol;
  flags: string;
  san: string;
  lan: string;
  before: string;
  after: string;
};

</script>



<style scoped>
table {
  overflow: auto;
}
</style>