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
    
    const url = 'ws://127.0.0.1:8000/ws/play/'+gameID + '/?' + store.token;
    console.log("url ", url);   
    const socket = new WebSocket(url);
    let boardAPI = ref({
      move: () => {},
      getMaterialCount: () => {},
    });
  

    const boardConfig = reactive({
      coordinates: true,
      viewOnly: false,
      animation: { enabled: true },
      draggable: { enabled: true },
      coordinates: true,
      events: {
        move: (from, to, promotion) => {
          console.log("Move event received:", from, to, promotion);
          handleMove(from, to, promotion); // Llamar a handleMove aquí
          materialDiff.value = boardAPI.value?.getMaterialCount().materialDiff;    
    },
      },
      trustAllEvents: true, 
    });


    function onRecieveMove(move) {
      console.log("onRecieveMove", move);
      // boardAPI?.move(move);
    }


    async function handleMove(from, to, promotion) {
      console.log("llama a move", from, to, promotion);
      if (boardAPI.value) { 
        boardAPI.value.move(from, to, promotion); 
      }

      moves.value.push({
        white: from, 
        black: to,
      });

      const message = JSON.stringify({
        'type': 'move',
        'from': from,
        'to': to,
        'playerID': store.userID,
        'promotion': promotion, 
      });
      await socket.send(message);
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
                if (store.userID === data.playerID) {
                  console.log('move data', data.from, data.to, data.promotion);

                  if (boardAPI.value) {
                    console.log('boardAPI.value', boardAPI.value);
                      boardAPI.value.move(data.from, data.to, data.promotion); 
                  }

                  onRecieveMove(uci_move);
                  handleMove(data.from, data.to, data.promotion);
                } else {
                  console.log('Error:', data.message);
                }
                
            } else if (data.type === 'error' ){
                console.log('Error:', data.message);
            }
        };  
    }

    onMounted(() => {
      connectWebSocket();
      // console.log(boardAPI?.getBoardPosition());
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