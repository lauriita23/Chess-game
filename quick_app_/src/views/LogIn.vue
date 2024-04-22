<template>
    <div>
        <div class="img">
            <img src="../assets/chess1.8ddb93c1.jpg" alt="myChess image 1" class="left-image" />
            <div class="form">
                <h1 class="title">Log In</h1>
                <p>
                    Do not have an account?  <a href="/sign-up">Sign Up</a>
                </p>
               
                <form @submit.prevent="logIn" class="form">
                    <input type="email" id="email" v-model="email" required placeholder="Email address"/>
                    <input type="password" id="password" v-model="password" required placeholder="Password"/>
                    <button type="submit">LOG IN</button>
                </form>
                <p>
                    Welcome to our chess page. If you want to know what led us to create another chess site, then read on.. <a href="/here">here</a>
                </p>
            </div>
        </div>
    </div>
</template>

<script>
import { ref }  from 'vue';
import { useRouter } from 'vue-router';
import { useTokenStore } from '@/stores/token';

export default {
    name: 'LogIn',
    setup() {
        const email = ref('');
        const password = ref('');
        const router = useRouter();

        const logIn = async () => {
            const formData = {
                username: email.value,
                password: password.value
            };
            
            const baseUrl = 'http://127.0.0.1:8000/api/v1';

          
            try{
                const response = await fetch(baseUrl + '/token/login', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData),
                });
                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail);
                }

                const store = useTokenStore();

                if (data && data.auth_token) {
                    store.setToken(data.auth_token);
                    router.push('/creategame');
                } else {
                    console.log('Error: Authentication token not found.');
                }
                
            } catch (error) {
                console.error('Error:', error);
            }
        };
        
        return {
            email,
            password,
            logIn
        };
    }
};
</script>

<style scoped>
.img {
    display: flex;
    justify-content: space-between;
    width: 70%; /* Ajustar tamaño */
}

.left-image {
    width: 50%;
    max-height: 80vh; /* Ajustar tamaño */
    object-fit: cover; /* Ajustar tamaño */
    margin-right: 20px; 
}

.form {
    width: 50%; /* Ajustar tamaño */
}

.form input,
.form button {
    margin-bottom: 10px;
    width: 100%;
    border-radius: 20px;
    padding: 10px; /* Añadir espacio interno */
    border: 1px solid #ccc; /* Añadir borde */
}

.form button {
    background-color: blue;
    color: white;
    border: none; /* Quitar borde */
    cursor: pointer; /* Cambiar cursor al pasar por encima */
}

.form button:hover {
    background-color: darkblue; /* Cambiar color al pasar por encima */
}

.title {
    font-family: Arial, Helvetica, sans-serif; /* Aplicar el tipo de letra definido en Bootstrap */
    text-align: center; /* Alinear al centro */
}
</style>
