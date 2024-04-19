<template>
    <div>
        <h1>LogOut</h1>
        <p>Are you sure you want to logout?</p>
        <button @click="logOut">Logout</button>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useTokenStore } from '@/stores/token';

export default {
    name: 'LogOut',
    setup() {
        const router = useRouter();
        const store = useTokenStore();

        const logOut = async () => {
            const baseUrl = process.env.VUE_APP_BASE_URL;
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
                router.push('/logout-success');

                // Redirect to home page after 5 seconds
                setTimeout(() => {
                    router.push('/');
                }, 5000);

            } catch (error) {
                console.error('Error:', error);
            }
        };

        return { logOut };
    }
}
</script>