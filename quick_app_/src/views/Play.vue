<script setup>
  import { ref, reactive, defineEmits, onMounted } from 'vue';
  import { TheChessboard } from 'vue3-chessboard';
  import 'vue3-chessboard/style.css';
  import { useTokenStore } from '@/stores/token';

  // Estado del juego
  const moves = ref([]);
  const store = useTokenStore();
  const gameID = store.gameID;
  const playerColor = store.color;
  const baseUrl = import.meta.env.VITE_DJANGOURL;
  const url = baseUrl + '/ws/play/' + store.gameID + '/?' + store.token;
  const socket = new WebSocket(url);
  let boardAPI;
  const checkmated = ref(false);
  const mated = ref('');

  console.log("el tablero es  ", store.board_state);

  // Configuración del tablero
  const boardConfig = reactive({
    coordinates: true,
    viewOnly: false,
    animation: { enabled: true },
    draggable: { enabled: true },
    fen: store.board_state,
    orientation: playerColor,
    events: {
      move: (from, to) => {
        console.log("Move event received:", from, to);
      },
    },
    trustAllEvents: true,
  });

  function handleCheckmate(isMated) 
  {
    checkmated.value = true;
    mated.value = isMated;
    alert(`${isMated} is mated`);
  }

  function handleStalemate ()
  {
    alert('Stalemate');
  }
  
  
  function handleDraw()
  {
    alert('Draw');
  }

  function handlePromotion () {
    alert('Promotion');
  }

  // Función para manejar el movimiento del jugador
  function handleMove(move) {

    console.log("Llega el movimiento a handle move:", move);

    // Procesar el movimiento y agregarlo a la lista de movimientos
    if(move.color === store.color.charAt(0))
    {
      moves.value.push({
        white: move.color === 'w' ? move.from + move.to : '',
        black: move.color === 'b' ? move.from + move.to : ''
      });


      // Enviar el movimiento al servidor si el socket está abierto
      if (socket.readyState === WebSocket.OPEN) {
        const promotion = move.promotion ? move.promotion : "";
        socket.send(JSON.stringify({
          'type': 'move',
          'from': move.from,
          'to': move.to,
          'playerID': store.userID,
          'promotion': promotion,
        }));
      } else {
        console.error('WebSocket is not open:', socket.readyState);
      }
    }

  }

  // Función para conectar el WebSocket
  function connectWebSocket() {
    socket.onopen = () => {
      console.log('WebSocket Client Connected');
    };

    socket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      console.log('Received:', data);

      if (data.type === 'game') {
        console.log("Game message received:", data);
      } else if (data.type === 'move') {
        console.log("Move message received:", data);
        const uci_move = data.from + data.to + (data.promotion ? data.promotion : "");
        if (store.userID !== data.playerID && boardAPI) {
          boardAPI.move(uci_move);
          moves.value.push({
              white: store.color === 'white' ? data.from + data.to : '',
              black: store.color === 'black' ? data.from + data.to : '',
          });
        }
      } else if (data.type === 'error') {
        console.log('Error message received:', data.message);
      }
    };
  }

  // Conectar el WebSocket cuando el componente está montado
  onMounted(() => {
    connectWebSocket();
  });
</script>



<template>
  <TheChessboard
      :board-config="boardConfig"
      :player-color="playerColor"
      @board-created="(api) => (boardAPI = api)"
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
<div
  v-if="checkmated && mated==='white'"
  data-cy="winMsg"
  class="alert alert-success"
  role="alert"
>
  Black Wins
  <button @click="router.push('/creategame')" data-cy=createGame-button-in-play>PLAY NEW GAME</button>
</div>
<div
  v-if="checkmated && mated==='black'"
  data-cy="winMsg"
  class="alert alert-success"
  role="alert"
>
  White Wins
  <button @click="router.push('/creategame')" data-cy=createGame-button-in-play>PLAY NEW GAME</button>
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