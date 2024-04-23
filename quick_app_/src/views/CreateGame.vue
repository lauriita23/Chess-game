<template>
    <div class="container">
      <h1 class="title">Create or Join a Game</h1>
      <div class="form-container">
        <form @submit.prevent="submitForm" class="form">
          <div class="form-group">
            <label for="gameType">Select Game Type:</label>
            <select id="gameType" v-model="selectedGameType" class="form-control">
              <option value="joinAny">Join any game</option>
              <option value="joinSpecific">Join specific game</option>
            </select>
          </div>
          <div v-if="selectedGameType === 'joinSpecific'" class="form-group">
            <label for="gameID">Enter Game ID:</label>
            <input type="text" id="gameID" v-model="gameID" class="form-control">
          </div>
          <button type="submit" class="btn btn-primary">Create/Join Game</button>
        </form>
      </div>
    </div>
  </template>
  

  <script>
  import { useTokenStore } from '@/stores/token';

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
        const store = useTokenStore();

        if (this.selectedGameType === 'joinAny') {
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
              throw new Error(data.detail);
            }
            
  
            //     gameID = game.id;
            //     const response2 = await fetch(baseUrl + '/ws/play/' + gameID, {
            //         method: 'POST',
            //         headers: {
            //           'Content-Type': 'application/json',
            //           'Authorization': 'token' + store.token
            //         },
            //         body: JSON.stringify({}),
            //     }); 

            //     const data2 = await response2.json();

            //     if (!response2.ok) {
            //       throw new Error(data2.detail);
            //     }


        
          } catch (error) {
            console.error('Error:', error);
          }
        

        } else if (this.selectedGameType === 'joinSpecific') {
          // Lógica para unirse a un juego específico
        }
      }
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

  .title
  {
    font-family: Arial, Helvetica, sans-serif;
  }
  </style>
  