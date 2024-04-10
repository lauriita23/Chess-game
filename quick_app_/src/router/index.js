import { createRouter, createWebHistory } from 'vue-router'

import LogIn from '../views/LogIn.vue'
import MyView from '../views/MyView.vue'


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/log-in',
            name: 'LogIn',
            component: LogIn
        },
        {
            path: '/my-view',
            name: 'MyView',
            component: MyView
        }
    ]
})

export default router