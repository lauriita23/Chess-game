
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
  <table class="tabla" data-cy="moveTable">
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
  <p>Game ID: {{ gameID }}</p>
</div>
</template>


<script setup>
    import { ref, reactive, defineEmits } from 'vue';
    import { onMounted, watch } from 'vue';
    import { TheChessboard } from 'vue3-chessboard';
    import 'vue3-chessboard/style.css';
    import { useRouter } from 'vue-router';
    import { useTokenStore } from '@/stores/token';

    const moves = ref([]);
    // Client will only be able to play white pieces.
    const router = useRouter();
    const store = useTokenStore();
    const gameID = store.gameID;
    
    const playerColor = 'white';
    // const url = baseUrl + 'play/'' + store.gameID.toString() + '/?' + store.token;
    const url = 'ws://127.0.0.1:8000/ws/play/'+gameID + '/?' + store.token;
    console.log("url ", url);   
    const socket = new WebSocket(url);
    let boardAPI = ref({
      fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', // the position to start from as a string
      orientation: 'white', // the orientation of the board
      turnColor: 'white', // the color which starts the game
      coordinates: true, // enable or disable board coordinates
      autoCastle: true, // simplify castling move
      viewOnly: false, // allow or disallow moves on the board
      disableContextMenu: false, // enable/ disable the context menu
      addPieceZIndex: false,
      blockTouchScroll: false,
      highlight: {
        lastMove: true, // highlight the last move on the board
        check: true, // highlight king in check
      },
      animation: { // modify piece animations
        enabled: true,
        duration: 200,
      },
      lastMove: undefined, // this should not be modified
      movable: {
        free: false, // set to true any move is allowed, if false only legal moves
        color: 'white',
        showDests: true,
        // dests:  TheChessboard.Board.legal_moves, 
        events: {},
        rookCastle: true,
      },
      premovable: {
        enabled: true,
        showDests: true,
        castle: true,
        events: {},
      },
      predroppable: {
        enabled: false,
        events: {},
      },
      draggable: {
        enabled: true,
        distance: 3,
        autoDistance: true,
        showGhost: true,
        deleteOnDropOff: false,
      },
      selectable: {
        enabled: true,
      },
      events: {},
      drawable: {
        enabled: true,
        visible: true,
        defaultSnapToValidMove: true,
        eraseOnClick: true,
        shapes: [],
        autoShapes: [],
        brushes: {
          green: { key: 'g', color: '#15781B', opacity: 1, lineWidth: 10 },
          red: { key: 'r', color: '#882020', opacity: 1, lineWidth: 10 },
          blue: { key: 'b', color: '#003088', opacity: 1, lineWidth: 10 },
          yellow: { key: 'y', color: '#e68f00', opacity: 1, lineWidth: 10 },
          paleBlue: { key: 'pb', color: '#003088', opacity: 0.4, lineWidth: 15 },
          paleGreen: { key: 'pg', color: '#15781B', opacity: 0.4, lineWidth: 15 },
          paleRed: { key: 'pr', color: '#882020', opacity: 0.4, lineWidth: 15 },
          paleGrey: {
            key: 'pgr',
            color: '#4a4a4a',
            opacity: 0.35,
            lineWidth: 15,
          },
        },
      },
    });

    const boardConfig = reactive({
        coordinates: true,
        viewOnly: false,
        animation: { enabled: true },
        draggable: { enabled: true },
        coordinates: true,
        // orientation: store,
        // fen: store.board_state,
        events: {
            move: (from, to, capture, sam) => {
                materialDiff.value = boardAPI.value?.getMaterialCount().n;
            },
        },
        trustAllEvents: true, 
    });

    let boardApi;

    function onBoardCreated(api) {
        boardApi = api;
        console.log(boardApi.getBoardPosition());
    }

    function onRecieveMove(move) {
        boardApi?.move(move);
    }

    function handleCheck(isInCheck) {
      alert(`${isInCheck} is in Check`);
    }

    function handleMove(move) {
      moves.value.push(move);
      const message = JSON.stringify({
        type: 'move',
        move: move,
      });
      socket.send(message);
    }

    function handleCheckmate(isMated) {
      alert(`${isMated} is mated`);
    }

    async function handlePromotion(promotion) {
      console.log(promotion);
      const message = JSON.stringify({
        type: 'promotion',
        promotion: promotion,
      });
    
      await socket.send(message);
    }

    function handleStalemate() {
      alert('Stalemate');
    }

    function handleDraw() {
      alert('Draw');
    }

    function connectWebSocket() {
        socket.onopen = () => {
            console.log('WebSocket Client Connected');
        };

        socket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            
            const uci_move = data.from + ' ' + data.to + ' ' + data.promotion;
            
            if (data.type == 'game')
            {
                console.log("message received");
                console.log(data);
            } else if (data.type = 'move')
            {
                if (store.userID == data.playerID)
                {
                    console.log('move data', data.from, data.to, data.promotion);
                    if (data.promotion != null)
                      handlePromotion(data.promotion);          
                    

                    // boardAPI.value?.move(uci_move);
                    onRecieveMove(uci_move);

                    moves.value.push({
                      white: data.from,
                      black: data.to,
                    });

                    const message = JSON.stringify({
                      type: 'move',
                      move: uci_move,
                    });

                    console.log("socket envia move", message);
                    socket.send(message);
                    
                }
            }
        };
  }

    onMounted(() => {
      connectWebSocket();
      console.log(boardApi?.getBoardPosition());
    });

</script>

<style scoped>
:host {
  background-color: black;
}

.tabla{
  position: absolute;
  top: 100px;
  right: 0;
}

table {
  overflow: auto;
}
</style>