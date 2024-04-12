<template>
    <div>
        <div class="form">
            <h1>Sign Up</h1>
            <form @submit.prevent="signUp">
                <input type="email" id="email" v-model="email" required/>
                <input type="password" id="password" v-model="password" required/>
                <input type="password" id="confirmPassword" v-model="confirmPassword" required/>
                <button type="submit">Sign Up</button>
            </form>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
    name: 'SignUp',
    setup() {
        const username = ref('');
        const email = ref('');
        const password = ref('');
        const confirmPassword = ref('');
        const router = useRouter();

        const signUp = async () => {
            const formData = {
                username: email.value,
                password: password.value
            };

            if (password.value !== confirmPassword.value) {
                // handle errors here
                console.error('Error: Passwords do not match.');
                return;
            }
            
            const baseUrl = process.env.VUE_APP_BASE_URL;
            // const baseUrl = 'http://localhost:8000/api/v1';
            const store = useTokenStore(); // no se si hace falta ?? 

            try {
                const response = await fetch(baseUrl + 'signup/', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData),
                });

                const data = await response.json();

                if (!response.ok) {
                    // handle errors here
                    throw new Error(data.detail);
                }

            } catch (error) {
                // handle errors here
                console.error('Error:', error);
            }

            // If the operation has been completed successfully, redirect to the login page
            router.push('/login');
        };

        return {
            username,
            email,
            password,
            confirmPassword,
            signUp
        };
    }, // setup end
}; // default end
</script>