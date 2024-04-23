<template>
    <div class="container">
      <div class="card">
        <div class="form">
          <h1 class="title">Log Out</h1>
          <p class="paragraph">
            You will be redirected to home in 5 seconds
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router';
  import { useTokenStore } from '@/stores/token';
  import { onMounted } from 'vue';
  
  
  export default {
    name: 'LogOut',
    setup() {
      const router = useRouter();
      const store = useTokenStore();
  
      const logOut = async () => {
        //const baseUrl = import.meta.env.VUE_APP_BASE_URL;
        const baseUrl = 'http://localhost:8000/api/v1';

        if(store.token == null) {
          alert("You cannot log out if you are not logged in");
          router.push('/log-in');
        }
            

        try {
          const response = await fetch(baseUrl + '/token/logout', {
            method: 'POST',
            headers: {
              'Authorization': 'token ' + store.token,
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            }
          });
          
          if (!response.ok) {
            throw new Error('Response not OK');
          }   
          
          store.token = null;
          
          
          setTimeout(() => {
            router.push('/log-in');
          }, 5000);
  
        } catch (error) {
          console.error('Error:', error);
        }
      };
      onMounted(logOut);
      return { logOut };
    }
  }
  </script>
  
  <style scoped>
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; 
  }
  
  .card {
    background-color: #f4f4f4;
    border: 1px solid #ddd; 
    border-radius: 5px; 
    padding: 60px; 
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
  }
  
  .form {
    text-align: center;
  }
  
  .title {
    font-family: Arial, Helvetica, sans-serif;
  }
  
  .paragraph {
    font-family: Arial, Helvetica, sans-serif;
  }
  </style>