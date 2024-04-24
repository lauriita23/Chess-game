const router = useRouter();
const materialDiff = ref(0);
const boardAPI = ref();
const store = useTokenStore();
const playerColor = store.color;
const showPlayerMesg = ref(false);
const playerMsfg = ref("Player Wins!");
const showNewGame = ref(false);
const moves = ref([]);
const promotion = ref("");
const baseUrl = ${import.meta.env.VITE_WS_URL};
const gameID = store.gameID;
const url = baseUrl + 'play/'' + store.gameID.toString() + '/?' + store.token;
const socket = new WebSocket(url);


const  boardConfig = {
    coordinates: true
    orientation: stores.
    fen: store.board_state,
    events: {
        move: (from, to, capture, sam) => {
            materialDiff.value = boardAPI.value?.getMaterialCount().n;
        },
    },
};


onMounted(() => {
    connectWebSocket();
});

on Updated(() => {
    scrollToBottom();
});

onUnmounted(() => {
    socket.close();
});

function beep() {
    var snd = new Audio('data:audio/wav;base64,//uQRAAAAWMSLwUIYAAsYkXgoQwAEaYLWfkWgAI0wWs/ItAAAGDgYtAgAyN+QWaAAihwMWm4G8QQRDiMcCBcHfQwA//uQRAAAAWMSLwUIYAAsYkXgoQwAEaYLWfkWgAI0wWs/ItAAAGDgYtAgAyN+QWaAAihwMWm4G8QQRDiMcCBcHfQwA//uQRAAAAWMSLwUIYAAsYkXgoQwAEaYLWfkWgAI0wWs/ItAAAGDgYtAgAyN+QWaAAihwMWm4G8QQRDiMcCBcHfQwA');
    snd.play();
}

function newGame() {
    router.push("/creategame");
}

function scrollToBottom() {
    const tableContainer = document.querySelector('table-contain......')
    if(tableContainer) {
        tableContainer.scrollTop = tableContainer.scrollHeight;
    }
}

function connectWebSocket() {
    socket.onopen = () => {
        console.log('WebSocket Client Connected');
    };

    socket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        const uci_move = data.form + data.to + data.promotion;
        if (data.type == 'game')
        {
            console.log("message received");
            console.log(data);
        }else if (data.type = 'move')
        {
            if (store.userID !== data.playerID)
            {
                console.log('move data', data.from, data.to, data.promotion);
                var result = boardAPI.value?.move(uci_move);
                console.log("BEEP");
                beep();
                console.log("result", result);
            }
        }
    };
}

// al final

console.log()
console.log()

if(move.color == store.color.charAt(0)){
    var promotion = "";
    if ("promotion" in move){
        console.log("promotion in move", move.promotion)
        promotion = move.promotion;
    }
}
await socket.send(JSON.stringify({
    'type': 'move',
    'from': move.from,
    'to': move.to,
    'promotion': promotion,
    'playerID': store.userID,
    'gameID': store.gameID,
    'token': store.token,
})

console.log()

------------------------------------------------------------------------
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
import { ref, reactive, defineEmits } from 'vue';
import { onMounted } from 'vue';
import { BoardApi, MoveEvent, PromotionEvent, TheChessboard, Color, Square, PieceSymbol } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';

const gameID = ref('');
const moves = ref([]);
// Client will only be able to play white pieces.
const playerColor = 'white';

const boardConfig = reactive({
  coordinates: true,
  viewOnly: false,
  animation: { enabled: true },
  draggable: { enabled: true },
  trustAllEvents: true, 
});

let boardApi;

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
  moves.value.push(move);
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