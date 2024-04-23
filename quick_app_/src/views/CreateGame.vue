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
            alert('Token:', store.token);
            /*el servidor verificar´a si hay juegos disponibles con un jugador ausente. Si no hay ninguno, crea un
            nuevo juego asignando aleatoriamente al jugador actual como jugador blanco o
            negro. Por el contrario si existe un juego creado con un s´olo jugador asignado
            se a˜nadir´a el jugador al juego existente. El API devuelve el game creado del
            cual se puede extraer el game.id, si se juega con blancas o con negras y cu´al
            es la posici´on inicial de las piezas puesto que la posici´on inicial de la partida
            puede no ser la est´andar. */
            const response = await fetch(baseUrl + '/games', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token' + store.token
              },
            }); 

            const data = await response.json();

            console.log('Data:', data);

        
          } catch (error) {
            console.error('Error:', error);
          }
        
        //   // si hay un juego con un jugador ausente, se unirá a ese juego
        //   try {
        //     const response = await fetch(baseUrl + '/ws/play/' + gameID, {

        //   });
        // } catch (error) {
        //   console.error('Error:', error);
        // }
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
  