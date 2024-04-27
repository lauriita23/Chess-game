<template>
  <div class="container">
    <h1 class="title">Create or Join a Game</h1>
    <div class="form-container">
      <form @submit.prevent="submitForm" class="form">
        <div class="form-group">
          <label for="selectGame">Select Game Type:</label>
          <select id="selectGame" v-model="selectedGameType" class="form-control">
            <option value="game_join_any">Join any game</option>
            <option value="join_specific_game">Join specific game (gameID required)</option>
          </select>
        </div>
        <div v-if="selectedGameType === 'join_specific_game'" class="form-group">
          <label for="gameID" data-cy="gameID">Enter gameID:</label>
          <input type="text" id="gameID" v-model="gameID" class="form-control" data-cy="gameID">
        </div>
        <button type="submit" class="btn btn-primary" data-cy="createGame-button"@click="createGame">Create/Join Game</button>
        <p v-if="errorMessage" data-cy="error-message">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useTokenStore } from '@/stores/token';
import { useRouter } from 'vue-router';

export default {
  name: 'CreateGame',
  setup() {
    const store = useTokenStore();
    const selectedGameType = ref('');
    const router = useRouter();
    const errorMessage = ref('');
    const gameID = ref('');

    const createGame = async () => {
     
      const formData = {
        selectedGameType: selectedGameType.value,
        gameID: gameID.value
      };

      if (selectedGameType.value === 'game_join_any') {
        const baseUrl = 'http://127.0.0.1:8000/api/v1';

        try {
          const response = await fetch(baseUrl + '/games/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'token ' + store.token
            },
            body: JSON.stringify({}),
          });

         
          const data = await response.json();
          

          if (!response.ok) {
            errorMessage.value = 'Error: Cannot create game';
            throw new Error(data.detail);
          }
          
          gameID.value = data['id']; 
          store.gameID = data['id'];

          if (data['whitePlayer'] > data['blackPlayer']){
            store.userID = data['whitePlayer'];
          } else {
            store.userID = data['blackPlayer'];
          }
          
          store.board_state = data['board_state'];
          
          router.push("/play");
        } catch (error) {
          errorMessage.value = 'Error: Cannot create game';
          console.error('Error:', error);
        }

      } else if (selectedGameType.value === 'join_specific_game') {
        // Logic to join a specific game
      }
    };

    return {
      errorMessage,
      gameID,
      selectedGameType,
      createGame,
    };
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.form-container {
  max-width: 400px;
  margin-top: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: blue;
  color: #fff;
  border: none;
  border-radius: 4px;
}

.btn:hover {
  background-color: blue;
}

.title {
  font-family: Arial, Helvetica, sans-serif;
}
</style>
