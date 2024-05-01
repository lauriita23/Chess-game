<template>
    <div>
        <div class="img">
            <img src="../assets/chess1.8ddb93c1.jpg" alt="myChess image 1" class="left-image" />
            <div class="form">
                <h1 class="title">Log In</h1>
                <p>
                    Do not have an account? <a href="/sign-up">Sign Up</a>
                </p>
                <form @submit.prevent="logIn" class="form">
                    <input type="email" id="email" v-model="email" required placeholder="Email address" data-cy="username"/>
                    <input type="password" id="password" v-model="password" required placeholder="Password" data-cy="password"/>
                    <p v-if="errorMessage" data-cy="error-message">{{ errorMessage }}</p>
                    <button type="submit" data-cy="login-button">LOG IN</button>
                </form>
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
        const errorMessage = ref('');

        const logIn = async () => {
            const formData = {
                username: email.value,
                password: password.value
            };
            
            //const baseUrl = 'http://127.0.0.1:8000/api/v1';
            const baseUrl = import.meta.env.VUE_APP_BASE_URL;

            try{
                const response = await fetch(baseUrl + '/mytokenlogin/', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData),
                });
                
                const data = await response.json();

                console.log("data", data)

                if (!response.ok) {
                    errorMessage.value = 'Error: Invalid username or password';
                    throw new Error(data);
                }

                const store = useTokenStore();

                if (data && data.auth_token) {
                    store.setToken(data.auth_token);
                    store.userID = data.user_id;
                    router.push('/creategame');
                } else {
                    errorMessage.value =  'Error: Invalid username or password';
                    console.log('Error: Authentication token not found.');
                }
                
            } catch (error) {
                console.error('Error:', error);
            }
        };
        
        return {
            email,
            password,
            logIn,
            errorMessage
        };
    }
};
</script>

<style scoped>
.img {
    display: flex;
    justify-content: space-between;
    width: 70%;
}

.left-image {
    width: 50%;
    max-height: 80vh;
    object-fit: cover; 
    margin-right: 20px; 
}

.form {
    width: 50%; 
}

.form input,
.form button {
    margin-bottom: 10px;
    width: 100%;
    border-radius: 20px;
    padding: 10px;
    border: 1px solid #ccc;
}

.form button {
    background-color: blue;
    color: white;
    border: none;
    cursor: pointer; 
}

.form button:hover {
    background-color: darkblue; 
}

.title {
    font-family: Arial, Helvetica, sans-serif; 
    text-align: center;
}
</style>
