<template>
    <div class="container">
            <div class="form">
                <h1 class="title">Log Out</h1>
                <p>Are you sure you want to logout?</p>
                <button @click="logOut">Logout</button>
            </div>
        </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { useTokenStore } from '@/stores/token';

export default {
    name: 'LogOut',
    setup() {
        const router = useRouter();
        const store = useTokenStore();

        const logOut = async () => {
            const baseUrl = import.meta.env.VUE_APP_BASE_URL;
            // const baseUrl = 'http://localhost:8000/api/v1';
            try {
                const response = await fetch(baseUrl + '/log-out', {
                    method: 'POST',
                    headers: {
                        'Authorization': 'token ' + store.token,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    }
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.detail);
                }
                if (data && data.message) {
                    console.log(data);
                } else {
                    console.log('Error: Authentication token not found.');
                }
                console.log('Success:');

                // Clear session variables
                store.clearToken();

                // Redirect to logout success page
                alert("You have been logged out successfully.")
                router.push('/log-in');

                // Redirect to home page after 5 seconds
                setTimeout(() => {
                    router.push('http://localhost:5173/log-in');
                }, 5000);

            } catch (error) {
                console.error('Error:', error);
            }
        };

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

.form {
    width: 50%;
}

.form p {
    margin-bottom: 20px;
}

.form button {
    margin-top: 10px;
    width: 100%;
    border-radius: 20px;
    padding: 10px;
    background-color: rgb(0, 0, 255);
    color: white;
    border: none;
    cursor: pointer;
}

.form button:hover {
    background-color: rgb(0, 0, 139);;
}

.title {
    font-family: Arial, Helvetica, sans-serif;
    text-align: center;
}
</style>
