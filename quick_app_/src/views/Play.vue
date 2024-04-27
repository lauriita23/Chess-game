<script setup>
    import { ref, reactive, defineEmits, watch, onMounted } from 'vue';
    import { TheChessboard } from 'vue3-chessboard';
    import 'vue3-chessboard/style.css';
    import { useRouter } from 'vue-router';
    import { useTokenStore } from '@/stores/token';

    const moves = ref([]);
    // Client will only be able to play white pieces.
    // const router = useRouter();
    const store = useTokenStore();
    const gameID = store.gameID;  
    const playerColor = 'white';
    const url = 'ws://127.0.0.1:8000/ws/play/'+ store.gameID + '/?' + store.token;
    
    const socket = new WebSocket(url);
    let boardAPI = ref({
      move: (move) => {
          //materialDiff.value = boardAPI.value?.getMaterialCount().materialDiff;    
      },
    });
  

    const boardConfig = reactive({
      coordinates: true,
      viewOnly: false,
      animation: { enabled: true },
      draggable: { enabled: true },
      fen: store.board_state,
      events: {
        move: (move) => {
          console.log("Move event received:", move.from, move.to);
      },
      },
      trustAllEvents: true, 
    });

    function onRecieveMove(from, to) {
      console.log("onRecieveMove", move);
      if (boardAPI.value)
        boardAPI.value.move(from, to);
    }

    async function handleMove(move) {
      
      console.log("llama a move", move.from, move.to);
    
      let promotion = "";
      if (move.san) {
        promotion = move.san.charAt(move.lan.length - 1);
        if (promotion === 'q' || promotion === 'r' || promotion === 'b' || promotion === 'n') {
          handlePromotion(promotion);
        } else {
          promotion = "";
        }
      }
        
      moves.value.push({
        white: move.color === 'w' ? move.from + move.to : '',
        black: move.color === 'b' ? move.from + move.to : ''
      });
      
      await socket.send(JSON.stringify({
        'type': 'move',
        'from': move['from'],
        'to': move['to'],
        'playerID': store.userID,
        'promotion': promotion,
      }));
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
            console.log('Received:', data);
            const uci_move = data.from + ' ' + data.to + ' ' + data.promotion;
            
            if (data.type === 'game')
            {
              console.log("message received");
              console.log(data);
            } 
            else if (data.type === 'move')
            {
                console.log('Move:', uci_move);
                if (store.userID !== data.playerID) {

                  if (boardAPI.value) {
                    boardAPI.value.move(uci_move);

                    if (store.color == 'white')
                      moves.value.push({
                        white: data.from + data.to,
                        black: '',
                      });
                    else 
                      moves.value.push({
                        white: '',
                        black: data.from + data.to,
                      });
                  }
                } 
                
            } else if (data.type === 'error' ){
                console.log('Error else:', data.message);
            }
        };  
    }

    onMounted(() => {
      connectWebSocket();
    });

</script>


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
      >
  </TheChessboard>
  <table class="tabla" data-cy="moveTable">
      <tr v-for="(move, index) in moves" :key="index">
        <td>{{ move.white}}</td>
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




<style scoped>
:host {
  background-color: black;
}

.tabla{
  position: absolute;
  top: 100px;
  right: 0px;
}

table {
  overflow: auto;
}
</style>