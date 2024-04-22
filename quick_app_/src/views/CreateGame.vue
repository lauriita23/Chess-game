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

    async submitForm() {
        if (this.selectedGameType === 'joinAny') {
            const baseUrl = 'http://127.0.0.1:8000/api/v1';
            // Check if there are available games with a missing player
            try {
                const response = await fetch(baseUrl + '/ws/play/' + this.gameID);
            
                const game = await response.json();

                // Verificara si hay juegos disponibles con un jugador ausente
                if (game.whitePlayer != None || game.blackPlayer != None){

                }
                    
                
                // Si no hay ninguno, crea un nuevo juego asignando aleatoriamente
                // al jugador actual como jugador blanco o negro
                if (game.length == 0) {
                    // New game is created if no available games are found
                    const response = await fetch('/games', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({status: , board_state: , id: this.gameID }),
                        // status, board state, end time.....???
                    });
                    const newGame = await response.json();
                    console.log('Created new game:', newGame);
                } else {
                    // Add player to existing game
                    const gameToJoin = game[0]; 

                    const joinGameResponse = await fetch(baseUrl + 'ws/play'+ gameToJoin, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({}),
                    })
                }
            }
             catch (error){
                console.error('Error:', error);
            }
        } else if (this.selectedGameType === 'joinSpecific') {
            // This is a non-functional option
            return;
        }
    }


    }
    };
</script>
