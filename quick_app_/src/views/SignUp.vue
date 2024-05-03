<template>
    <div>
        <div class="img">
            <img src="../assets/chess1.8ddb93c1.jpg" alt="myChess image 1" class="left-image" />
            <div class="form">
                <h1 class="title">myChess Sign Up page</h1>
                <form @submit.prevent="signUp" class="form">
                    <input type="email" id="email" v-model="email" required placeholder="Email address" data-cy="username"/>
                    <input type="password" id="password" v-model="password" required placeholder="Password" data-cy="password1"/>
                    <input type="password" id="confirmPassword" v-model="confirmPassword" required placeholder="Confirm Password" data-cy="password2"/>
                    <button type="submit" data-cy="signup-button">SIGN UP</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
    name: 'SignUp',
    setup() {
        const email = ref('');
        const username = ref('');
        const password = ref('');
        const confirmPassword = ref('');
        const router = useRouter();

        const signUp = async () => {
            const formData = {
                email: email.value,
                username: email.value,
                password: password.value,
                confirmPassword: confirmPassword.value
            };

            if (password.value !== confirmPassword.value) {
                // handle errors here
                alert("Passwords do not match.");
                console.error('Error: Passwords do not match.');
                return;
            }
            
            const baseUrl = import.meta.env.VITE_DJANGOURL;

            try {
                const response = await fetch(baseUrl + '/users/', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({email: formData.email, username: formData.email, password: formData.password}),
                });
                
                if (!response.ok) {
                    // handle errors here
                    throw new Error(data);
                }


                const data = await response.json();

            } catch (error) {
                // handle errors here
                console.error('Error:', error);
            }

            router.push('/log-in');
        };

        return {
            email,
            username,
            password,
            confirmPassword,
            signUp
        };
    }, // setup end
}; // default end
</script>


<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; 
}

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