<template>
    <div>
        <div class="img">
            <img src="../assets/chess1.8ddb93c1.jpg" alt="myChess image 1" class="left-image" />
            <div class ="form">
                <h1>myChess Sign Up page</h1>
                <form @submit.prevent="signUp" class="form">
                    <input type="email" id="email" v-model="email" required placeholder="Email address"/>
                    <input type="password" id="password" v-model="password" required placeholder="Password"/>
                    <input type="password" id="confirmPassword" v-model="confirmPassword" required placeholder="Confirm Password"/>
                    <button type="submit">SIGN UP</button>
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
        const password = ref('');
        const confirmPassword = ref('');
        const router = useRouter();

        const signUp = async () => {
            const formData = {
                email: email.value,
                password: password.value,
                confirmPassword: confirmPassword.value
            };

            if (password.value !== confirmPassword.value) {
                // handle errors here
                console.error('Error: Passwords do not match.');
                return;
            }
            
            const baseUrl = 'http://127.0.0.1:8000/api/v1';
            // const store = useTokenStore(); // no se si hace falta ?? 

            try {
                const response = await fetch(baseUrl + '/sign-up', {
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
            router.push('/log-in');
        };

        return {
            email,
            password,
            confirmPassword,
            signUp
        };
    }, // setup end
}; // default end
</script>


<style scoped>
.img {
    display: flex;
    justify-content: space-between;
}

.container {
    display: flex;
    justify-content: center;
    align-items: flex-start; 
}

.left-image {
    width: 50%;
    margin-right: 20px; 
}

.content {
    width: 50%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}

.form {
    display: flex;
    flex-direction: column;
    align-items: flex-start; 
}

.form input,
.form button {
    margin-bottom: 10px;
    width: 100%;
    border-radius: 20px;
}

.form button {
    background-color: blue;
    color: white;
}
</style>