<template>
    <div>
        <div class="form">
            <h1>Log In</h1>
            <form @submit.prevent="logIn">
                <input type="email" id="email"
                    v-model="email" required/>
                <input type="password" id="password"
                    v-model="password" required/>
                <button type="submit">Log In</button>
            </form>
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
            
            // const baseUrl = import.meta.env.VUE_APP_BASE_URL;
            const baseUrl = 'http://127.0.0.1:8000/api/v1';
            
          
            try{
                const response = await fetch(baseUrl + '/token/login', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        // 'Authorization': 'token' + store.token
                    },
                    body: JSON.stringify(formData),
                });
                const data = await response.json();

                if (!response.ok) {
                    // handle errors here
                    throw new Error(data.detail);
                }

                const store = useTokenStore();

                if (data && data.auth_token) {
                    store.setToken(data.auth_token);
                    // En caso de exito el usuario debe ser redirigido creategame
                    router.push('/creategame');
                } else {
                    console.log('Error: Authentication token not found.');
                }
                
            } catch (error) {
                // handle errors here
                console.error('Error:', error);
            }
        };
        
        // return reactive variables and functions
        return {
            email,
            password,
            logIn
        };
    }
};
</script>
