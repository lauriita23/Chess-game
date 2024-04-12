<template>
    <div>
        <div class="form">
            <h1>Log IN</h1>
            <form @submit.prevent="logIn">
                <input type="username" id="username"
                    v-model="username" required/>
                <input type="password" id="password"
                    v-model="password" required/>
                <button type="submit">Log In</button>
            </form>
        </div>
    </div>
</template>


<script>
import { ref }  from 'vue';
import { useTokenStore } from '@/stores/token';

export default {
    name: 'LogIn',
    setup() {
        const username = ref('');
        const password = ref('');

        const logIn = async () => {
            const fromData = {
                username: username.value,
                password: password.value
            };
            const baseUrl = 'http://localhost:8000/api/v1';
            const store = useTokenStore();
            
            try{
                //fetch returns a Promise that resolves to a Response object
                // token/login is defined by djoser
                const response = await fetch(baseUrl + 'token/login', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                        // 'Authorization': 'token' + store.token
                    },
                    body: JSON.stringify(formData),
                });
                const data = await response.json();

                if (!response.ok) {
                    // handle errors here
                    throw new Error(data.detail);
                }

                if (data && data.auth_token) {
                    store.setToken(data.auth_token);
                } else {
                    console.log('Error: Authentication token not found.');
                }
                
            } catch (error) {
                // handle errors here
                console.error('Error:', error);
            }
            
            // En caso de exito el usuario debe ser redirigido creategame
            router.push('/creategame');
        
        };
        // return reactive variables
        return {
            username,
            password,
            logIn
        };
    }, // setup end
}; // default end
</script>
