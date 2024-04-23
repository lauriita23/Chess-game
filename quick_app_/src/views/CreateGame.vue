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
                'Authorization': 'token' + store.token
              },
              body: JSON.stringify({}),
            }); 

            const data = await response.json();

            if (!response.ok) {
              throw new Error(data.detail);
            }

            console.log('Data:', data);
            
            /*el servidor verificar´a si hay juegos disponibles con un jugador ausente. */
            if (data.length !== 0) {
              data.forEach(async game => {
                  if (!game.whitePlayer || !game.blackPlayer) {
                    console.log('Game without whitePlayer or blackPlayer:', game);
                    try {
                        gameID = game.id;
                        const response2 = await fetch(baseUrl + '/ws/play/' + gameID, {
                            method: 'POST',
                            headers: {
                              'Content-Type': 'application/json',
                              'Authorization': 'token' + store.token
                            },
                            body: JSON.stringify({}),
                        }); 

                        const data2 = await response2.json();

                        if (!response2.ok) {
                          throw new Error(data2.detail);
                        }

                    } catch (error) {
                        console.log('Error', error);
                    }
                    //hay  mas de 1 juego y no estan libres => creo un juego
                  } else {
                    
                      /* Si no hay ninguno, crea un
                    nuevo juego asignando aleatoriamente al jugador actual como jugador blanco o
                    negro. Por el contrario si existe un juego creado con un s´olo jugador asignado
                    se a˜nadir´a el jugador al juego existente. El API devuelve el game creado del
                    cual se puede extraer el game.id, si se juega con blancas o con negras y cu´al
                    es la posici´on inicial de las piezas puesto que la posici´on inicial de la partida
                    puede no ser la est´andar.*/
                      
                    console.log("no hay juegos sin un jugador");
                    const response = await fetch(baseUrl + '/games/', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json',
                      'Authorization': 'token' + store.token
                    },
                    body: JSON.stringify({}),
                  }); 

                  const data = await response.json();
                  }
              });
            } 
        
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
  