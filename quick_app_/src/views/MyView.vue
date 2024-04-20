<template>
    <div>
        <div class="form">
            <h1>My View</h1>
            {{ msg }}
        </div>
    </div>
</template>


<script>
import { ref, onBeforeMount } from 'vue';
import { useTokenStore } from '@/stores/token';

export default {
    name: 'MyView',
    setup() {
        const msg = ref('');

        const myView = async () => {
            // do not hard code URLs
            // read them from the enviroment
            
            const baseUrl = import.meta.env.VUE_APP_BASE_URL;
            // const baseUrl = 'http://localhost:8000/api/v1';
            const store = useTokenStore();


            try {
                const response = await fetch(baseUrl + 'myclassView/', {
                    method: 'GET',
                    headers: {
                        'Authorization': 'token' + store.token,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    }
                });
                const data = await response.json();

                if (!response.ok) {
                    // handle errors here
                    // throw new Error(data.detail);
                }

                if (data && data.message) {
                    msg.value = data.message;
                    console.log(data);
                } else {
                    console.log('Error: Authentication token not found.');
                    // handle errors here
                }

                console.log('Success:');
                // jump to play page
            } catch (error) {
                // handle errors here
                console.error('Error:', error);
            }
        };

        onBeforeMount(() => {
            myView();
        });

        return {
            msg,
        };
    }, // setup end
}; // default end
</script>