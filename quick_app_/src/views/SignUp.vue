<template>
    <div>
        <div class="img">
            <img src="../assets/chess1.8ddb93c1.jpg" alt="myChess image 1" class="left-image" />
            <div class ="form">
                <h1 class="title">myChess Sign Up page</h1>
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
            
            const baseUrl = import.meta.env.VUE_APP_BASE_URL;
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
            alert('User created successfully!')
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
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* Centrar verticalmente */
}

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