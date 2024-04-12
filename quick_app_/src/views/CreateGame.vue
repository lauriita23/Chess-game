<template>
  <div>
    <h1>Create or Join a Game</h1>
    <form @submit.prevent="submitForm">
      <label for="gameType">Select Game Type:</label>
      <select id="gameType" v-model="selectedGameType">
        <option value="joinAny">Join any game</option>
        <option value="joinSpecific">Join specific game</option>
      </select>
      <div v-if="selectedGameType === 'joinSpecific'">
        <label for="gameID">Enter Game ID:</label>
        <input type="text" id="gameID" v-model="gameID">
      </div>
      <button type="submit">Create/Join Game</button>
    </form>
  </div>
</template>

<script>
export default {
    name: 'CreateGame',
    data() {
    return {
        selectedGameType: 'joinAny',
        gameID: ''
    };
    },
    methods: {
    // setup() {
        
    // },


    submitForm() {
        if (this.selectedGameType === 'joinAny') {
            // Check if there are available games with a missing player
            if (ChessGame.objects.filter(id=gameID).exists() == false) {
                // New game is created if no available games are found
                ChessGame.objects.create(id=gameID)
            } else {
                // Add player to existing game
                ChessGame.objects.filter(id=gameID).update(player2=player)
            }
        } else if (this.selectedGameType === 'joinSpecific') {
            // This is a non-functional option
            return;
        }
    }


    }
    };
</script>
