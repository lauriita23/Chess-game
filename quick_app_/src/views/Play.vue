
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
  <table data-cy="moveTable">
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
    const url = 'http://127.0.0.1:8000/ws/play/'+gameID+'/';
    const socket = new WebSocket(url);
    let boardAPI = ref({
        move: () => {},
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

    function handlePromotion(promotion) {
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
            const uci_move = data.form + data.to + data.promotion;
            if (data.type == 'game')
            {
                console.log("message received");
                console.log(data);
            } else if (data.type = 'move')
            {
                if (store.userID !== data.playerID)
                {
                    console.log('move data', data.from, data.to, data.promotion);
                    var result = boardAPI.value?.move(uci_move);
                    console.log("result", result);
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
.chessboard-container {
  background-color: black;
}

table {
  overflow: auto;
}
</style>