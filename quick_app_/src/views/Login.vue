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
import { useTok } from '@';

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
                const response = await fetch(baseUrl + 'token/login', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                        // 'Authorization': 'token' + store.token
                    },
                    body: JSON.stringify(formData)
                });
                const data = await response.json();
                
            }
        
        }
    }

        
}
    


</script>
