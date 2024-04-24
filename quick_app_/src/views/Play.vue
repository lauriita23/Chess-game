<script setup>
    import { ref, reactive, defineEmits } from 'vue';
    import { onMounted } from 'vue';
    import { TheChessboard } from 'vue3-chessboard';
    import 'vue3-chessboard/style.css';
    import { useRouter } from 'vue-router';

    const gameID = ref('');
    const moves = ref([]);
    // Client will only be able to play white pieces.
    const playerColor = 'white';
    const router = useRouter();

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

<style scoped>
.chessboard-container {
  background-color: black;
}

table {
  overflow: auto;
}
</style>